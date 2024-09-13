import uuid
from datetime import datetime

from factory import (
    LazyAttribute,
    LazyFunction,
    Sequence,
    SubFactory,
    post_generation,
    SelfAttribute,
)
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyInteger, FuzzyText
from faker import Faker
from faker.providers import misc
from pytz import UTC

from app.model_instance.schemas import ModelInstance


from .database import Session

fake = Faker()
fake.add_provider(misc)


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class TimeStampBaseFactory(BaseFactory):
    """Timestamp Base Factory."""

    created_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    updated_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))


class ModelInstanceFactory(BaseFactory):
    """ModelInstance Factory."""

    official_key = FuzzyText(prefix="sk-")
    endpoint = FuzzyText()
    instance = Sequence(lambda n: f"instance-{n}")
    model = Sequence(lambda n: f"model-{n}")
    active = FuzzyChoice([True, False])

    class Meta:
        """Factory Configuration."""

        model = ModelInstance
