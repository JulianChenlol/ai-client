from .factory import FactoryProducer
from .constants import LLM
from typing import List
from .models.chat import Dialog


def completion(model_name: str, messages: List[Dialog], stream: bool):
    return FactoryProducer.get_factory(LLM).get_model(model_name).complete(messages, stream)
