from typing import List, Optional

from fastapi import APIRouter

from pydantic import BaseModel
from starlette.responses import JSONResponse


from app.model.llm_model.router import router as llm_model_router
from app.factories.model.router import router as model_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

# WARNING: Don't use this unless you want unauthenticated routes
authenticated_api_router = APIRouter()


# )


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


api_router.include_router(llm_model_router, prefix="/llm_models", tags=["llm_models"])
api_router.include_router(model_router, prefix="/models", tags=["models"])
