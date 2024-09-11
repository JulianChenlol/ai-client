from fastapi import APIRouter
from pydantic_core import ValidationError, InitErrorDetails
from typing import List

from app.database.core import DbSession
from app.exceptions import InvalidUsernameError, InvalidPasswordError, InvalidConfigurationError
from .models import UserLogin, UserLoginResponse, UserRead, UserCreate
from .service import get_by_email, create

from app.api_key.models import ApiKeyRead
from app.api_key.service import get_by_user as get_apikeys_by_user
from app.post.models import PostRead
from app.post.service import get_by_user as get_posts_by_user

auth_router = APIRouter()
user_router = APIRouter()


@auth_router.post("/login", response_model=UserLoginResponse)
def login_user(
    user_in: UserLogin,
    db_session: DbSession,
):
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user and user.check_password(user_in.password):
        return {"token": user.token}

    raise ValidationError.from_exception_data(
        title=UserLogin.__name__,
        line_errors=[
            InitErrorDetails(
                type=InvalidUsernameError.code,
                loc=("username",),
                input=user_in.email,
            ),
            InitErrorDetails(
                type=InvalidPasswordError.code,
                loc=("password",),
                input=user_in.password,
            ),
        ],
    )


@user_router.post(
    "",
    response_model=UserRead,
)
def create_user(
    user_in: UserCreate,
    db_session: DbSession,
):
    """Creates a new user."""
    user = get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise ValidationError.from_exception_data(
            title=UserLogin.__name__,
            line_errors=[
                InitErrorDetails(
                    type=InvalidConfigurationError.code,
                    loc=("username",),
                    input=user_in.email,
                ),
            ],
        )

    user = create(db_session=db_session, user_in=user_in)
    return user


@user_router.get("/{user_id}/apikeys", response_model=List[ApiKeyRead])
def get_apikeys(user_id: int, db_session: DbSession) -> List[ApiKeyRead]:
    return get_apikeys_by_user(db_session=db_session, user_id=user_id)


@user_router.get("/{user_id}/posts", response_model=List[PostRead])
def get_posts(user_id: int, db_session: DbSession) -> List[PostRead]:
    return get_posts_by_user(db_session=db_session, user_id=user_id)
