# Ćwiczenia praktyczne 2 – deklaracja modeli i # tworzenie bazy danych 
# W nowym projekcie (nie powiązanym z poprzednim zadaniem) zainstaluj SQLAlchemy, przygotuj nowe połączenie z bazą danych SQLite.
# Stwórz dwie tabele: 
# 1. Experiment z kolumnami: id: int, title: string, created_at: datetime, type: int, finished: boolean (domyślnie False).
# 2. DataPoint z kolumnami: id: int, real_value: float, target_value: float.
# Stwórz wszystkie zdefiniowane tabele wraz z plikiem bazy danych. 
# Na tym etapie jeszcze nie definiujmy relacji w tabelach. 
import os
from datetime import datetime
from sqlalchemy import create_engine, Integer,String, DateTime, Boolean, Float,select, update, delete, func, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column,relationship
import random

if os.path.exists("test.db"):
    os.remove("test.db")

engine= create_engine("sqlite:///test.db", echo=True)

class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__= "experiment"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    title: Mapped[str]= mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.now)
    type: Mapped[int]= mapped_column(Integer)
    finished: Mapped[bool] =mapped_column(Boolean, default=False)


class DataPoint(Base):
    __tablename__= "datapoint"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    real_value:  Mapped[float]= mapped_column(Float)
    target_value: Mapped[float]=mapped_column(Float)

Base.metadata.create_all(engine)

#------ 
# Ćwiczenia praktyczne 3
# Rozszerz program z poprzednich ćwiczeń by: 
# 1. Dodał 2 wiersze do tabeli Experiments. 
# 2. Dodał 10 wierszy do tabeli DataPoints.
# 3. Pobrać dodane przed chwilą dane i wyświetlił informację o nich. 
# 4. Zaktualizował wszystkie wierszy Experiments poprzez ustawienie finished na True.
# 5. Usunął wszystkie wiersze z obu tabel.

def rand_point():
    return DataPoint(real_value=random.random(), target_value=random.random() )

with Session(engine) as s:
    s.add_all(
        [Experiment(title="A", type=1, finished=True),
         Experiment(title="B", type=2)]
        + [rand_point() for _ in range(10)])
    s.commit()

with Session(engine) as s:
    experiments= s.scalars(select(Experiment)).all()
    datapoints= s.scalars(select(DataPoint)).all()

    print(f"Experiment: {len(experiments)} wierszy")
    for e in experiments:
        print(f"  id={e.id}, title={e.title}, type={e.type}, finished={e.finished}, created_at={e.created_at}")

    print(f"DataPoint: {len(datapoints)} wierszy")
    for dp in datapoints:
        print(f"  id={dp.id}, real_value={dp.real_value}, target_value={dp.target_value}")

with Session(engine) as s:
    s.execute(update(Experiment).values(finished=True))
    s.commit()

with Session(engine) as s:
    s.execute(delete(Experiment))
    s.execute(delete(DataPoint))
    s.commit()

#---------------------------------------
# Ćwiczenia 4
# Usuń poprzednią bazę danych (usuń sam plik bazy danych). 
# Dodaj relację jeden do wielu tak, by jeden Experiment posiadał wiele DataPoint’ów.
# Odpal program i stwórz bazę danych ponownie, popraw skrypt
# tworzący elementy w bazie tak, by tworzyć 20 DataPoints– 10 dla jednego eksperymentu, 10 dla drugiego

engine.dispose() #zamknie polaczenia starego engine
del engine
if os.path.exists("test.db"):
    os.remove("test.db")

engine= create_engine("sqlite:///test.db", echo=True)

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

Base.metadata.create_all(engine)

def rand_point():
    return DataPoint(real_value=random.random(), target_value=random.random() )

with Session(engine) as s:
    expa= Experiment(title="A", type=1, finished=True, points=[rand_point() for _ in range(10)])
    expb= Experiment(title="B", type=2,points=[rand_point() for _ in range(10)])
    s.add_all([expa,expb])
    s.commit()

with Session(engine) as s:
    for exp in s.scalars(select(Experiment)).all():
        print(f'{exp.title}: {len(exp.points)}  punktow')

#---------------------------------------------------------------
# Ćwiczenia praktyczne 5
# Używając agregacji pobierz sumę i średnią wszystkich DataPoint dla  każdego eksperymentu.

with Session(engine) as s:
    stmt=(select(Experiment.title,func.sum(DataPoint.real_value),func.avg(DataPoint.real_value))
        .join(DataPoint, DataPoint.experiment_id== Experiment.id)
        .group_by(Experiment.id))
    
    for title, suma, srednia in s.execute(stmt):
        print(f"{title}: suma={suma:.4f}, średnia= {srednia:.4f}")


#ZADANIE Z MIGRACJI W PLIKU: sqlmigracja.py