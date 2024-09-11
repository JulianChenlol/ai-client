from fastapi import APIRouter
from typing import List

from .service import (
    get,
    add_users,
    get_by_user,
    create,
    update,
    generate_api_key,
)
from app.model_instance.service import add_model_instances, get_by_apikey
from .models import ApiKeyCreate, ApiKeyRead, ApiKeyUpdate
from app.database.core import DbSession

router = APIRouter()


@router.post("", response_model=ApiKeyCreate)
def create_apikey(api_key_in: ApiKeyCreate, db_session: DbSession):
    if not api_key_in.key:
        api_key_in.key = generate_api_key()
    return create(db_session=db_session, api_key_in=api_key_in)


@router.get("/{api_key_id}", response_model=ApiKeyRead)
def get_apikey(api_key_id: int, db_session: DbSession):
    return get(db_session=db_session, api_key_id=api_key_id)


@router.put("/{api_key_id}", response_model=ApiKeyRead)
def update_apikey(api_key_id: int, api_key_in: ApiKeyUpdate, db_session: DbSession):
    api_key = get(db_session=db_session, api_key_id=api_key_id)
    return update(db_session=db_session, api_key_in=api_key_in, api_key=api_key)


@router.post("/{api_key_id}/users")
def add_users_to_apikey(user_ids: List[int], api_key_id: int, db_session: DbSession):
    add_users(db_session=db_session, user_ids=user_ids, api_key_id=api_key_id)


@router.get("/users/{user_id}", response_model=List[ApiKeyRead])
def get_apikey_by_user(user_id: int, db_session: DbSession) -> List[ApiKeyRead]:
    return get_by_user(db_session=db_session, user_id=user_id)


@router.post("/{api_key_id}/model_instandces")
def add_model_instances_to_apikey(
    model_instance_ids: List[int], api_key_id: int, db_session: DbSession
):
    add_model_instances(
        db_session=db_session, model_instance_ids=model_instance_ids, api_key_id=api_key_id
    )


@router.get("/{api_key_id}/model_instandces")
def get_model_instances_by_apikey(api_key_id: int, db_session: DbSession):
    return get_by_apikey(db_session=db_session, api_key_id=api_key_id)
