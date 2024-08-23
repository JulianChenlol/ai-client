from fastapi import APIRouter, HTTPException, status

from .service import create, get, update, delete
from app.database.core import DbSession
from app.database.service import CommonParameters, search_filter_sort_paginate
from .models import (
    ModelInstanceCreate,
    ModelInstanceRead,
    ModelInstanceUpdate,
    ModelInstancePagination,
)

router = APIRouter()


@router.get("page", response_model=ModelInstancePagination)
def get_all_model_instances(common: CommonParameters):
    return search_filter_sort_paginate(model="ModelInstance", **common)


@router.post("/create", response_model=ModelInstanceCreate)
def create_model_instance(db_session: DbSession, model_instance_in: ModelInstanceCreate):
    return create(db_session=db_session, model_instance_in=model_instance_in)


@router.get("/{model_instance_id}", response_model=ModelInstanceRead)
def get_model_instance(db_session: DbSession, model_instance_id: int):
    return get(db_session=db_session, model_instance_id=model_instance_id)


@router.put("/update/{model_instance_id}", response_model=ModelInstanceRead)
def update_model_instance(
    db_session: DbSession, model_instance_id: int, model_instance_in: ModelInstanceUpdate
):
    model_instance = get(db_session=db_session, model_instance_id=model_instance_id)
    if not model_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A ModelInstance with this id does not exist."}],
        )
    return update(
        db_session=db_session, model_instance=model_instance, model_instance_in=model_instance_in
    )


@router.delete("/{model_instance_id}")
def delete_model_instance(db_session: DbSession, model_instance_id: int):
    model_instance = get(db_session=db_session, model_instance_id=model_instance_id)
    if not model_instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A ModelInstance with this id does not exist."}],
        )
    delete(db_session=db_session, model_instance_id=model_instance_id)
