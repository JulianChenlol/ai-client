from typing import List
import requests
import json
from ..models.base import ChatModel
from ..models.chat import Dialog

PROMPT_TEMPLATE = """<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant"""
# URL = "http://10.40.22.45:8000/completion"
TIMEOUT = 30


class QwenModel(ChatModel):

    def __init__(self) -> None:
        super().__init__(apikey=None, model_name="qwen")

    def get_model_config(self):
        return {
            "n_predict": 128,
            "temperature": 0.8,
        }

    def transform_messages(self, messages: List[Dialog]) -> str:
        prompt = ""
        system_prompt = self.get_chat_prompt_system()
        for dialog in messages:
            if dialog.role == "system":
                system_prompt.content += dialog.content
            elif dialog.role == "user":
                prompt += "<|im_start|>user\n" + dialog.content + "<|im_end|>\n"
            elif dialog.role == "assistant":
                prompt += "<|im_start|>assistant\n"
                if dialog.content:
                    prompt += dialog.content + "<|im_end|>\n"
        return "<|im_start|>user\n" + system_prompt + "<|im_end|>\n" + prompt

    def get_data(self, messages: List[Dialog], stream: bool):
        config = self.get_model_config()
        data = {
            "prompt": self.transform_messages(messages),
            "n_predict": config.get("n_predict", 128),
            "temperature": config.get("temperature", 0.8),
            "stream": stream,
            "stop": ["<|im_end|>"],
        }
        return json.dumps(data)

    def format_prompt(self, prompt: str):
        return PROMPT_TEMPLATE.format(prompt=prompt)

    def complete(self, messages: List[Dialog], stream: bool):
        response = requests.post(
            url=self.url,
            headers={"Content-Type": "application/json"},
            data=self.get_data(messages=messages, stream=stream),
            timeout=TIMEOUT,
        )
        if response.status_code == 200:
            return response.json()
