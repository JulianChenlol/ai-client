from fastapi import APIRouter, HTTPException, status
from typing import List

from .service import create, get, update, delete, add_model_instances, get_by_apikey, get_by_user
from app.database.core import DbSession
from app.database.service import CommonParameters, search_filter_sort_paginate
from .models import (
    ModelInstanceCreate,
    ModelInstanceRead,
    ModelInstanceUpdate,
    ModelInstancePagination,
)

router = APIRouter()


@router.get("/page", response_model=ModelInstancePagination)
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


@router.post("/add_model_instances")
def add_model_instances_to_apikey(
    model_instance_ids: List[int], api_key_id: int, db_session: DbSession
):
    add_model_instances(
        db_session=db_session, model_instance_ids=model_instance_ids, api_key_id=api_key_id
    )


@router.get("/get_by_api_key/{api_key_id}")
def get_model_instances_by_apikey(api_key_id: int, db_session: DbSession):
    return get_by_apikey(db_session=db_session, api_key_id=api_key_id)


@router.get("/get_by_user/{user_id}")
def get_model_instances_by_user(user_id: int, db_session: DbSession):
    return get_by_user(db_session=db_session, user_id=user_id)
