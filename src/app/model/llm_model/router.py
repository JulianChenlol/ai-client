from fastapi import APIRouter, HTTPException, status
from app.models import PrimaryKey
from app.database.core import DbSession
from app.database.service import CommonParameters, search_filter_sort_paginate
from .models import LlmModelPagination, LlmModelCreate, LlmModelRead, LlmModelUpdate
from .service import create, get, update, delete

router = APIRouter()


@router.get("/page", response_model=LlmModelPagination)
def get_all_llm_models(common: CommonParameters):
    """Get all LLM models"""
    return search_filter_sort_paginate(model="LlmModel", **common)


@router.post("/create", response_model=LlmModelCreate)
def create_llm_model(db_session: DbSession, llm_model_in: LlmModelCreate):
    """Create a new LLM model"""
    return create(db_session=db_session, llm_model_in=llm_model_in)


@router.get("/{llm_model_id}", response_model=LlmModelRead)
def get_llm_model(db_session: DbSession, llm_model_id: int):
    """Get a LLM model"""
    return get(db_session=db_session, llm_model_id=llm_model_id)


@router.put("/update/{llm_model_id}", response_model=LlmModelRead)
def update_llm_model(db_session: DbSession, llm_model_id: PrimaryKey, llm_model_in: LlmModelUpdate):
    """Update a LLM model"""
    llm_model = get(db_session=db_session, llm_model_id=llm_model_id)
    if not llm_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A Model with this id does not exist."}],
        )
    return update(db_session=db_session, llm_model=llm_model, llm_model_in=llm_model_in)


@router.delete("/{llm_model_id}")
def delete_llm_model(db_session: DbSession, llm_model_id: int):
    """Delete a LLM model"""
    llm_model = get(db_session=db_session, llm_model_id=llm_model_id)
    if not llm_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A Model with this id does not exist."}],
        )
    delete(db_session=db_session, llm_model_id=llm_model_id)
