from sqlalchemy.orm import Session
from .models import ModelInstanceCreate, ModelInstanceUpdate
from .schemas import ModelInstance


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
