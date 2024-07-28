from fastapi import APIRouter

from app.database.service import CommonParameters, search_filter_sort_paginate
from .models import LlmModelPagination

router = APIRouter()


@router.get("", response_model=LlmModelPagination)
def get_all_llm_models(common: CommonParameters):
    """Get all LLM models"""
    return search_filter_sort_paginate(model="LlmModel", **common)
