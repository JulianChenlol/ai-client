from fastapi import APIRouter
from typing import List

from .service import add_users, get_by_user, create, generate_api_key
from .models import ApiKeyCreate
from app.database.core import DbSession

router = APIRouter()


@router.post("/create")
def create_apikey(api_key_in: ApiKeyCreate, db_session: DbSession):
    if not api_key_in.key:
        api_key_in.key = generate_api_key()
    return create(db_session=db_session, api_key_in=api_key_in)


@router.post("/add_users")
def add_users_to_apikey(user_ids: List[int], api_key_id: int, db_session: DbSession):
    add_users(db_session=db_session, user_ids=user_ids, api_key_id=api_key_id)


@router.get("/get_by_user")
def get_apikey_by_user(user_id: int, db_session: DbSession):
    return get_by_user(db_session=db_session, user_id=user_id)
