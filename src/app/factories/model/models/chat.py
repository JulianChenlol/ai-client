from typing import Literal
from openai.types.chat.chat_completion import (  # noqa F401
    ChatCompletion,
    Choice,
    ChatCompletionMessage,
)
from pydantic import BaseModel
from typing import List


class Dialog(BaseModel):
    role: Literal["system", "user", "assistant"] = "user"
    content: str = "Who are you?"


class ChatRequest(BaseModel):
    model: str
    messages: List[Dialog]
    stream: bool


class ChatResponse(ChatCompletion):
    pass
