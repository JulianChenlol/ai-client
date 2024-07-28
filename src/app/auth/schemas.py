from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.core import Base
from app.models import TimeStampMixin
from app.config import APP_JWT_ALG, APP_JWT_EXP, APP_JWT_SECRET
import bcrypt
import jwt


class AppUser(Base, TimeStampMixin):
    __table_args__ = {"schema": "app_core"}

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)
    last_mfa_time = Column(DateTime, nullable=True)
    experimental_features = Column(Boolean, default=False)

    # relationships
    events = relationship("Event", backref="app_user")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=APP_JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, APP_JWT_SECRET, algorithm=APP_JWT_ALG)
