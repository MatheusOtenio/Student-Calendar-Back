from sqlalchemy import Column, Integer, String, DateTime, Date, ARRAY
from database import Base

class Tarefa(Base):
    __tablename__ = "tarefas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(500))
    data_limite = Column(DateTime)

class Cronograma(Base):
    __tablename__ = "cronogramas"
    
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    tarefas_ids = Column(ARRAY(Integer))