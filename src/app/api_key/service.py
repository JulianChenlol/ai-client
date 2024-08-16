from typing import Optional
from sqlalchemy.orm import Session
from typing import List
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from jose import JWTError, jwt
from jose.exceptions import JWKError

from .schemas import ApiKey, UserApiKey
from .models import ApiKeyCreate, ApiKeyUpdate
from app.utils.log_util import logger
from config import APP_JWT_SECRET


def generate_api_key() -> str:
    """Generates a new api key"""


def check_api_key(request: Request) -> Optional[ApiKey]:
    """Check if the api key is valid"""
    authorization: str = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        logger.exception(
            f"Malformed authorization header. Scheme: {scheme} Param: {param} Authorization: {authorization}"
        )
        return

    token = authorization.split()[1]

    try:
        data = jwt.decode(token, APP_JWT_SECRET)
    except (JWKError, JWTError):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=[{"msg": "Could not validate credentials"}],
        ) from None

    return get_by_key(
        db_session=request.state.db,
        key=data["key"],
    )


def get_by_key(*, db_session: Session, key: str) -> Optional[ApiKey]:
    """Returns a ApiKey object based on the given key"""
    return db_session.query(ApiKey).filter(ApiKey.key == key).first()


def get(*, db_session: Session, api_key_id: int) -> Optional[ApiKey]:
    """Returns a ApiKey object based on the given the id"""
    return db_session.query(ApiKey).filter(ApiKey.id == api_key_id).first()


def get_all(*, db_session: Session) -> List[Optional[ApiKey]]:
    """Returns all ApiKey objects"""
    return db_session.query(ApiKey).all()


def create(*, db_session: Session, api_key_in: ApiKeyCreate) -> ApiKey:
    """Creates a new ApiKey object"""
    api_key = ApiKey(**api_key_in.model_dump())
    db_session.add(api_key)
    db_session.commit()
    return api_key


def update(*, db_session: Session, api_key: ApiKey, api_key_in: ApiKeyUpdate) -> ApiKey:
    """Updates a ApiKey object"""
    api_key_data = api_key.dict()
    update_data = api_key_in.model_dump(exclude_unset=True)
    for field in api_key_data:
        if field in update_data:
            setattr(api_key, field, update_data[field])
    db_session.commit()
    return api_key


def delete(*, db_session: Session, api_key_id: int):
    """Deletes a ApiKey object"""
    api_key = db_session.query(ApiKey).filter(ApiKey.id == api_key_id).first()
    db_session.delete(api_key)
    db_session.commit()


def add_users(*, db_session: Session, user_ids: List[int], api_key_id: int):
    """Adds users to an api key"""
    db_session.add_all(UserApiKey(user_id=user_id, api_key_id=api_key_id) for user_id in user_ids)
    db_session.commit()


def get_by_user(*, db_session: Session, user_id: int) -> List[ApiKey]:
    """Returns a ApiKey object based on the given user id"""
    return db_session.query(UserApiKey).filter(UserApiKey.user_id == user_id).all()
