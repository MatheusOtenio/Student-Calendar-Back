from fastapi import FastAPI, Depends, HTTPException
from typing import List
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from sqlalchemy.orm import Session
import crud
import models

app = FastAPI()

# Schemas Pydantic
class TarefaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    data_limite: datetime

class TarefaCreate(TarefaBase):
    pass

class Tarefa(TarefaBase):
    id: int

    class Config:
        orm_mode = True

class CronogramaBase(BaseModel):
    data: date
    tarefas_ids: Optional[List[int]] = None

class CronogramaCreate(CronogramaBase):
    pass

class Cronograma(CronogramaBase):
    id: int

    class Config:
        orm_mode = True

# Endpoints Tarefas
@app.get("/tarefas", response_model=List[Tarefa])
async def read_tarefas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tarefas = crud.get_tarefas(db)
    return tarefas

@app.post("/tarefas", response_model=Tarefa)
async def create_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    return crud.create_tarefa(db, tarefa.dict())

@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
async def update_tarefa(tarefa_id: int, tarefa: TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = crud.update_tarefa(db, tarefa_id, tarefa.dict())
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.delete("/tarefas/{tarefa_id}")
async def delete_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = crud.delete_tarefa(db, tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return {"ok": True}

# Endpoints Cronogramas
@app.get("/cronogramas", response_model=List[Cronograma])
async def read_cronogramas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cronogramas = crud.get_cronogramas(db)
    return cronogramas

@app.post("/cronogramas", response_model=Cronograma)
async def create_cronograma(cronograma: CronogramaCreate, db: Session = Depends(get_db)):
    return crud.create_cronograma(db, cronograma.dict())