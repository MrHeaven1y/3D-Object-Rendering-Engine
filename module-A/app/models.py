import uuid
from sqlalchemy import Column, String, Integer, JSON, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

def gen_id():
    return str(uuid.uuid4())


class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, nullable=False)
    config = Column(JSON, nullable=False)
    seed = Column(Integer, nullable=True)
    status = Column(String, nullable=False, default="queued")
    progress = Column(Integer, nullable=False, default=0)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=None)
    finished_at = Column(DateTime(timezone=True), server_default=None)