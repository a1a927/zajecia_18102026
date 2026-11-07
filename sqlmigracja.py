#-----------------------------------------------
# Ćwiczenia praktyczne 5 – relacja wiele-do wielu oraz migracja bazy danych
# Usuń poprzednią bazę danych (usuń sam plik bazy danych). 
# Zainstaluj i zainicjuj Alembic w programie z poprzednich ćwiczeń.
# Wygeneruj pierwszą migrację i zaaplikuj ją na bazie danych.
# Dodaj nową tabelę Subject z kolumnami: id: int, gdpr_accepted: bool(domyślnie na False). 
# Stwórz relację wiele-do-wielu pomiędzy Subject i Experiment.
# Wygeneruj nową migrację i zaaplikuj ją na baize danych.
import os
from datetime import datetime
from sqlalchemy import create_engine, Integer,String, DateTime, Boolean, Float,select, update, delete, func, ForeignKey,Table,Column
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column,relationship
import random

#TERMINAL: Remove-Item test.db -ErrorAction SilentlyContinue


class Base(DeclarativeBase):
    pass

class Experiment(Base):
    __tablename__ = "experiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title:Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)
    points: Mapped[list["DataPoint"]] = relationship(back_populates="experiment")

class DataPoint(Base):
    __tablename__ = "datapoint"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped["Experiment"] = relationship(back_populates="points")



experiment_subject = Table(
    "experiment_subject",
    Base.metadata,
    Column("experiment_id",Integer, ForeignKey("experiment.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subject.id"), primary_key=True))


class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    gdpr_accepted: Mapped[bool]= mapped_column(Boolean, default=False)
    experiments: Mapped[list["Experiment"]]= relationship(secondary=experiment_subject, back_populates="subjects")

