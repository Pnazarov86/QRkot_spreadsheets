from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract_model import AbstractModel


class Donation(AbstractModel):
    """Модель пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
