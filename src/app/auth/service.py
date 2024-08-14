from typing import Annotated, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from jose.exceptions import JWKError
from fastapi import HTTPException, Depends


from .schemas import AppUser
from .models import UserRegister, UserCreate
from app.utils.log_util import logger
from config import APP_JWT_SECRET


def get_by_email(*, db_session: Session, email: str) -> Optional[AppUser]:
    """Returns a user object based on user email."""
    return db_session.query(AppUser).filter(AppUser.email == email).one_or_none()


def create(*, db_session: Session, user_in: UserRegister | UserCreate) -> AppUser:
    """Creates a new dispatch user."""
    # pydantic forces a string password, but we really want bytes
    password = bytes(user_in.password, "utf-8")

    # create the user
    user = AppUser(**user_in.model_dump(exclude={"password"}), password=password)

    db_session.add(user)
    db_session.commit()
    return user


def get_or_create(*, db_session: Session, user_in: UserRegister) -> AppUser:
    """Gets an existing user or creates a new one."""
    user = get_by_email(db_session=db_session, email=user_in.email)

    if not user:
        try:
            user = create(db_session=db_session, user_in=user_in)
        except IntegrityError:
            db_session.rollback()
            logger.exception(f"Unable to create user with email address {user_in.email}.")

    return user


def get_current_user(request: Request) -> AppUser:
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

    return get_or_create(
        db_session=request.state.db,
        user_in=UserRegister(email=data["email"]),
    )


CurrentUser = Annotated[AppUser, Depends(get_current_user)]
