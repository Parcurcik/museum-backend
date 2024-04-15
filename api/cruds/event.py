from api.cruds.base import Base, with_model

from api.models import EventORM


@with_model(EventORM)
class Event(Base):
    pass
