from sqlalchemy import Boolean, Column, Integer, String, create_engine, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    benchmark_id = Column(String)
    task_id = Column(String)
    task_version = Column(String)
    model = Column(String)
    temperature = Column(Float)
    timestamp = Column(String)
    response = Column(String)
    completion_tokens = Column(Integer)
    success = Column(Boolean)


def create_database():
    engine = create_engine("sqlite:///benchmark_results.db")
    Base.metadata.create_all(engine)


def recreate_database():
    engine = create_engine("sqlite:///benchmark_results.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
