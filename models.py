from sqlalchemy import Column, Integer, String, DateTime, Date, ARRAY, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    
    tarefas = relationship("Tarefa", back_populates="user")
    cronogramas = relationship("Cronograma", back_populates="user")

class Tarefa(Base):
    __tablename__ = "tarefas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(500))
    data_limite = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="tarefas")

class Cronograma(Base):
    __tablename__ = "cronogramas"
    
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    tarefas_ids = Column(ARRAY(Integer))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="cronogramas")