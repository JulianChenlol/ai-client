from fastapi import APIRouter, HTTPException, status
from .models.chat import ChatRequest, ChatResponse
from .factory import FactoryProducer
from .constants import LLM

router = APIRouter()


@router.post("/completion", response_model=ChatResponse)
def complete(chat_request: ChatRequest):
    model_instance = FactoryProducer.get_factory(LLM).get_model(chat_request.model)
    if not model_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "This model does not exist."}],
        )
    else:
        return model_instance.complete(chat_request.messages, chat_request.stream)
