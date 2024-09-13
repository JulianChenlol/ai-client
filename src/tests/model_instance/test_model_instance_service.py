from sqlalchemy.orm import Session
from app.model_instance.schemas import ModelInstance


def test_get(session: Session, model_instance: ModelInstance):
    from app.model_instance.service import get

    t_model_instance = get(db_session=session, model_instance_id=model_instance.id)
    assert t_model_instance.id == model_instance.id
