""" Server module for the Moth project. """

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass
import time
import zmq
from moth.driver import ModelDriver
from moth.message import (
    HandshakeMsg,
    ClassificationResultMsg,
    HandshakeResponseMsg,
    HeartbeatMsg,
    Msg,
    ObjectDetectionResultMsg,
    parse_message,
)
from moth.message.exceptions import MothMessageError


@dataclass
class Model:
    """Holds information about a model that is connected to the server."""

    id: str
    task_type: str
    output_classes: Optional[List[str]] = None

    def serialize(self):
        return {
            "id": self.id,
            "taskType": self.task_type,
            "outputClasses": self.output_classes,
        }

    @staticmethod
    def deserialize(json) -> "Model":
        return Model(
            id=json["id"],
            task_type=json["taskType"],
            output_classes=json["outputClasses"],
        )


class Server:
    """Server class that accepts connections from models."""

    HEARTBEAT_TIMEOUT = 5
    HEARTBEAT_INTERVAL = 1

    def __init__(self, port: int = 7171):
        self.port = port
        self._stop = False
        self._driver_factory: Optional[Callable[[HandshakeMsg], ModelDriver]] = None
        self._drivers: Dict[bytes, ModelDriver] = {}
        self._models: Dict[bytes, Model] = {}
        self._on_model_change_handler: Optional[Callable[[List[Model]], None]] = None
        self._heartbeats: Dict[bytes, float] = {}

    def driver_factory(self, func: Callable[[HandshakeMsg], ModelDriver]):
        """
        Annotation to provide driver factory function.
        For every incoming model connection, this factory is called to get a driver for
        that model.
        """
        self._driver_factory = func
        return func

    def start(self):
        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        socket.bind(f"tcp://*:{self.port}")
        self._recv_loop(socket)

    def stop(self):
        self._stop = True

    def _recv_loop(self, socket: zmq.Socket):
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        last_heartbeat = time.time()
        print("Server listening...")
        while not self._stop:
            # handle input
            events = dict(poll.poll(1000))
            if events:
                identity = socket.recv()
                msg_bytes = socket.recv()

                try:
                    message = parse_message(msg_bytes)
                    if isinstance(message, HandshakeMsg) and self._driver_factory:
                        driver = self._driver_factory(message)
                        identity_str = identity.decode("utf-8")
                        model = Model(
                            id=identity_str,
                            task_type=message.task_type,
                            output_classes=message.output_classes,
                        )
                        self._drivers[identity] = driver
                        self._models[identity] = model
                        self._heartbeats[identity] = time.time()
                        if self._on_model_change_handler:
                            self._on_model_change_handler(
                                list(self._models.values())
                            )  # Pass the list of current drivers
                        print(f"MUT connected: {identity_str}")
                        # Send a handshake response
                        socket.send(identity, zmq.SNDMORE)
                        socket.send(HandshakeResponseMsg().serialize_envelope())

                    if isinstance(message, ClassificationResultMsg):
                        if identity in self._drivers:
                            self._drivers[identity].on_model_result(message)

                    if isinstance(message, ObjectDetectionResultMsg):
                        if identity in self._drivers:
                            self._drivers[identity].on_model_result(message)

                    if isinstance(message, HeartbeatMsg):
                        self._heartbeats[identity] = time.time()

                except MothMessageError as err:
                    print(err)
                except Exception as err:
                    print(err)

            # Check if we need to send heartbeats
            if last_heartbeat + Server.HEARTBEAT_INTERVAL < time.time():
                last_heartbeat = time.time()
                for identity in self._drivers:
                    socket.send(identity, zmq.SNDMORE)
                    socket.send(HeartbeatMsg().serialize_envelope())

            disconnected = []
            for identity in self._drivers:
                next_prompt = self._drivers[identity].next_model_prompt()
                if next_prompt is not None:
                    socket.send(identity, zmq.SNDMORE)
                    socket.send(next_prompt.serialize_envelope())
                # Check heartbeat status
                if identity in self._heartbeats:
                    if (
                        self._heartbeats[identity] + Server.HEARTBEAT_TIMEOUT
                        < time.time()
                    ):
                        # Mark as diconnected
                        disconnected.append(identity)

            # Remove disconnected models
            for identity in disconnected:
                self._drivers.pop(identity)
                self._models.pop(identity)
                self._heartbeats.pop(identity)
                if self._on_model_change_handler:
                    self._on_model_change_handler(list(self._models.values()))
                print(f"MUT disconnected: {identity.decode('utf-8')}")

        socket.close()

    def on_model_change(self, func: Callable[[List[Model]], None]):
        """
        Annotation to provide a function that is called when the list of connected models changes.
        """
        self._on_model_change_handler = func
        return func
