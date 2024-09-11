from typing import Optional, List
from sqlalchemy.orm import Session
from pydantic_core import ValidationError, InitErrorDetails
import requests
import telnetlib


from .schemas import LlmModel
from .models import LlmModelCreate, LlmModelUpdate, LlmModelRead

from app.exceptions import NotFoundError
from app.utils.log_util import logger


def check_service_health(host: str, port: int) -> bool:
    try:
        telnetlib.Telnet(host=host, port=port, timeout=2)
        logger.info(f"Service is healthy for {host}:{port}")
        return True
    except Exception as e:
        logger.error(f"Service is unhealthy for {host}:{port}, error: {e}")
        return False


def check_api_health(host: str, port: int, fail_on_no_slot=False) -> bool:
    url = f"{host}:{port}/health"
    params = {}
    if fail_on_no_slot:
        params["fail_on_no_slot"] = "1"

    try:
        response = requests.get(url, params=params)
        status_code = response.status_code
        data = response.json()

        if status_code == 200:
            if data["status"] == "ok":
                logger.info("Service is healthy and ready.")
            elif data["status"] == "no slot available":
                logger.warning("Service is up, but no slots are available.")
            return True
        elif status_code == 503 and data["status"] == "loading model":
            logger.error("Service is loading the model.")
            return True
        elif status_code == 500 and data["status"] == "error":
            logger.error("Service encountered an error while loading the model.")
            return False
        else:
            logger.error(f"Unhandled status code {status_code} with response {data}")
            return True

    except requests.RequestException as e:
        logger.error(f"Failed to connect to service: {e}")


def get(*, db_session: Session, llm_model_id: int) -> Optional[LlmModel]:
    """Returns a LlmModel object based on the given the id"""
    return db_session.query(LlmModel).filter(LlmModel.id == llm_model_id).first()


def get_by_name(*, db_session: Session, name: str) -> Optional[LlmModel]:
    """Returns a LlmModel object based on the given name"""
    return db_session.query(LlmModel).filter(LlmModel.name == name).one_or_none()


def get_by_name_or_raise(*, db_session: Session, llm_model_in: LlmModelRead) -> LlmModel:
    """Returns the llm_model specified or raises ValidationError."""
    llm_model = get_by_name(db_session=db_session, name=llm_model_in.name)
    if llm_model is None:
        raise ValidationError.from_exception_data(
            title=LlmModelRead.__name__,
            line_errors=[
                InitErrorDetails(type=NotFoundError, loc=("llm_model",), input=llm_model_in.name)
            ],
        )
    return llm_model


def get_all(*, db_session: Session) -> List[Optional[LlmModel]]:
    """Returns all LlmModel objects"""
    return db_session.query(LlmModel).all()


def create(*, db_session: Session, llm_model_in: LlmModelCreate) -> LlmModel:
    """Creates a new LlmModel object"""
    llm_model = LlmModel(**llm_model_in.model_dump())
    db_session.add(llm_model)
    db_session.commit()
    return llm_model


def get_or_create(*, db_session: Session, llm_model_in: LlmModelCreate) -> LlmModel:
    """Returns the llm_model specified or creates a new one."""
    if llm_model_in.id:
        q = db_session.query(LlmModel).filter(LlmModel.id == llm_model_in.id)
    else:
        q = db_session.query(LlmModel).filter_by(**llm_model_in.model_dump(exclude={"id"}))
    instance = q.first()
    if instance:
        return instance
    return create(db_session=db_session, llm_model_in=llm_model_in)


def update(*, db_session: Session, llm_model: LlmModel, llm_model_in: LlmModelUpdate) -> LlmModel:
    """Updates a LlmModel object"""
    llm_model_data = llm_model.dict()
    update_data = llm_model_in.model_dump(exclude_unset=True)
    for field in llm_model_data:
        if field in update_data:
            setattr(llm_model, field, update_data[field])
    db_session.commit()
    return llm_model


def delete(*, db_session: Session, llm_model_id: int):
    """Deletes a LlmModel object"""
    llm_model = db_session.query(LlmModel).filter(LlmModel.id == llm_model_id).first()
    db_session.delete(llm_model)
    db_session.commit()
