from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.constants import DEFAULT_AMOUNT
from app.core.db import Base


class AbstractModel(Base):
    """Абстрактная модель."""
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=DEFAULT_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
