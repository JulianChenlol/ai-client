from abc import ABC, abstractmethod
from .repository.llm.qwen_model import QwenModel
from app.plugins.app_nacos.manager import get_service_instance


class IFactory(ABC):
    @abstractmethod
    def get_model(self, model_type: str):
        pass


class LlmFactory(IFactory):
    def get_model(self, model_type: str):
        url = get_service_instance(model_type)
        if not url:
            return None
        if model_type == "qwen":
            return QwenModel(url)
        else:
            return None


class EmbeddingFactory(IFactory):
    def get_model(self, model_type: str):
        return None


class RerankerFactory(IFactory):
    def get_model(self, model_type: str):
        return None


class FactoryProducer:

    @staticmethod
    def get_factory(factory_type: str):
        if factory_type == "llm":
            return LlmFactory()
        elif factory_type == "embedding":
            return EmbeddingFactory()
        elif factory_type == "reranker":
            return RerankerFactory()
        else:
            return None
