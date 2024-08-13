from typing import Literal
from openai.types.chat.chat_completion import (  # noqa F401
    ChatCompletion,
    Choice,
    ChatCompletionMessage,
)


class Dialog(ChatCompletionMessage):
    role: Literal["system", "user", "assistant"] = "user"
    content: str = "Who are you?"
