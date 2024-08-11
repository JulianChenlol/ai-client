import datetime
from typing import List
from .chat import Dialog


class BaseModel:
    def __init__(self, apikey: str, model_name: str) -> None:
        self._apikey = apikey
        self._model_name = model_name

    @property
    def model_name(self):
        return self._model_name


class ChatModel(BaseModel):

    def get_chat_prompt_system(self) -> Dialog:
        today = datetime.date.today()
        chat_prompt_system = (
            "You are ZephyrGPT, a large language model trained by Zephyr. Do not mention Others like OpenAI."
            "You are chatting with the user via the ZephyrGPT Web."
            "This means most of the time your lines should be a sentence or two,"
            "unless the user's request requires reasoning or long-form outputs."
            "Never use emojis, unless explicitly asked to."
            "Knowledge cutoff: 2023-04"
            "Current date: {}.\n".format(today)
        )
        return Dialog(role="system", content=chat_prompt_system)

    def stream_complete(self, messages: List[Dialog]):
        pass

    def complete(self, messages: List[Dialog]):
        pass


class EmbeddingModel(BaseModel):

    def get_embedding(self, text: List[str]):
        pass


class RerankModel(BaseModel):

    def get_rerank(self, query: str, text: List[str]):
        pass
