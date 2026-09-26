from sqlalchemy import Column, Integer, ForeignKey, Date, Time
from app.database.connection import Base


class Detection(Base):

    __tablename__ = "detections"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    camera_id = Column(
        Integer,
        ForeignKey("cameras.id"),
        nullable=False
    )

    date = Column(
        Date,
        nullable=False
    )

    heure = Column(
        Time,
        nullable=False
    )