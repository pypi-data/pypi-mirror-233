
# MOdel Test Harness (Moth)

Simple way to interrogate your AI model from a separate testing application

# Quickstart

`moth server <folder path>`

`moth client`

# Client



Simplest possible classification model client.
``` python
from moth import Moth
from moth.message import ImagePromptMsg, ClassificationResultMsg, HandshakeTaskTypes

moth = Moth("my-ai", task_type=HandshakeTaskTypes.CLASSIFICATION)

@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    return ClassificationResultMsg(prompt_id=prompt.id, class_name="cat") # Most pictures are cat pictures 

moth.run()
```

ClassificationResultMsg can optionally include a confidence value

``` python
ClassificationResultMsg(prompt_id=prompt.id, class_name="cat", confidence=0.9)
```

Simplest possible object detection model client.
``` python
from moth import Moth
from moth.message import ImagePromptMsg, ObjectDetectionResultMsg, ObjectDetectionResult, HandshakeTaskTypes

moth = Moth("my-ai", task_type=HandshakeTaskTypes.OBJECT_DETECTION)

@moth.prompt
def on_prompt(prompt: ImagePromptMsg):
    # TODO: Do smart AI here
    # Make a list of ObjectDetectionResults
    l = []
    l.append(ObjectDetectionResult(0, 0, 50, 50, class_name="cat", class_index=0, confidence=0.9))
    l.append(ObjectDetectionResult(10, 10, 50, 35, class_name="dog", class_index=1, confidence=0.1))
    return ObjectDetectionResultMsg(prompt_id=prompt.id, object_detection_results=l)
 

moth.run()
```

You can also define a set of client output classes that get handed over to the server.
``` python
moth = Moth("my-ai", task_type=HandshakeTaskTypes.CLASSIFICATION, output_classes=["cat", "dog"])
```

# Server

Simplest possible server.
``` python
from moth.server import Server
from moth.message import HandshakeMsg

class ModelDriverImpl(ModelDriver):
    # TODO: Implement your model driver here
    pass

server = Server(7171)

@server.driver_factory
def handle_handshake(handshake: HandshakeMsg) -> ModelDriver
    return ModelDriverImpl()
```

You can also register to keep an up to date list of connected models.
``` python
from moth.server import Model

@server.on_model_change
def handle_model_change(model_list: List[Model]):
    print(f"Connected models: {model_list}")
```
