from typing import List
import requests
import json
from app.factories.model.models.base import ChatModel
from app.factories.model.models.chat import Dialog
from app.config import CUSTOM_LLM_URL

TIMEOUT = 30


class CustomModel(ChatModel):

    def __init__(self, url) -> None:
        self._url = url
        super().__init__(apikey=None, model="custom")

    def get_model_config(self):
        return {
            "n_predict": 128,
            "temperature": 0.8,
        }

    def get_data(self, messages: List[Dialog], stream: bool):
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [message.model_dump() for message in messages],
            "temperature": 0.8,
            "stream": stream,
        }
        return json.dumps(data)

    def complete(self, messages: List[Dialog], stream: bool):
        response = requests.post(
            url=self._url,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=self.get_data(messages=messages, stream=stream),
            timeout=TIMEOUT,
        )
        if response.status_code == 200:
            return response.json()


if __name__ == "__main__":
    model = CustomModel(url=CUSTOM_LLM_URL)
    messages = [
        Dialog(role="user", content="Who are you?"),
    ]
    print(model.complete(messages=messages, stream=False))
