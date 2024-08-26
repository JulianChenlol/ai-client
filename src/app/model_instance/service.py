from sqlalchemy.orm import Session
from typing import List, Optional

from .models import ModelInstanceCreate, ModelInstanceUpdate
from .schemas import ModelInstance
from app.api_key.schemas import ModelInstanceApiKey
from app.utils.tools import timer


def create(*, db_session: Session, model_instance_in: ModelInstanceCreate) -> ModelInstance:
    """Creates a new ModelInstance object"""
    model_instance = ModelInstance(**model_instance_in.model_dump())
    db_session.add(model_instance)
    db_session.commit()
    return model_instance


def get(*, db_session: Session, model_instance_id: int) -> ModelInstance:
    """Returns a ModelInstance object based on the given the id"""
    return db_session.query(ModelInstance).filter(ModelInstance.id == model_instance_id).first()


def get_all(*, db_session: Session) -> list[ModelInstance]:
    """Returns all ModelInstance objects"""
    return db_session.query(ModelInstance).all()


def update(
    *, db_session: Session, model_instance: ModelInstance, model_instance_in: ModelInstanceUpdate
) -> ModelInstance:
    """Updates a ModelInstance object"""
    model_instance_data = model_instance.dict()
    update_data = model_instance_in.model_dump(exclude_unset=True)
    for field in model_instance_data:
        if field in update_data:
            setattr(model_instance, field, update_data[field])
    db_session.commit()
    return model_instance


def delete(*, db_session: Session, model_instance_id: int):
    """Deletes a ModelInstance object"""
    model_instance = (
        db_session.query(ModelInstance).filter(ModelInstance.id == model_instance_id).first()
    )
    db_session.delete(model_instance)
    db_session.commit()


@timer
def add_model_instances(*, db_session: Session, model_instance_ids: List[int], api_key_id: int):
    """Adds model instances to an api key"""
    db_session.bulk_save_objects(
        ModelInstanceApiKey(model_instance_id=model_instance_id, api_key_id=api_key_id)
        for model_instance_id in model_instance_ids
    )
    db_session.commit()


def get_by_apikey(*, db_session: Session, api_key_id: int) -> List[Optional[ModelInstance]]:
    """Returns model instances based on the given api key id"""
    return (
        db_session.query(ModelInstance)
        .join(ModelInstanceApiKey)
        .filter(ModelInstanceApiKey.api_key_id == api_key_id)
    ).all()
