from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import date, datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import crud
import models
from auth import Token, UserCreate, User, authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

# Configuração de CORS para permitir requisições do frontend
origins = [
    "http://localhost",
    "http://localhost:8501",  # Porta padrão do Streamlit
    "https://student-calendar-v2.streamlit.app",  # Domínio do frontend em produção
    "*",  # Temporariamente permitir todas as origens durante desenvolvimento
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Endpoints de Autenticação
@app.post("/api/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/auth/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já registrado")
    if user.email:
        db_user_email = crud.get_user_by_email(db, email=user.email)
        if db_user_email:
            raise HTTPException(status_code=400, detail="Email já registrado")
    try:
        return crud.create_user(db=db, user_data=user.dict())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de duplicação detectado no banco de dados")

@app.get("/api/auth/me", response_model=User)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

# Endpoints Tarefas
@app.get("/tarefas", response_model=List[Tarefa])
async def read_tarefas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    tarefas = crud.get_tarefas(db)
    return tarefas

@app.post("/tarefas", response_model=Tarefa)
async def create_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    tarefa_data = tarefa.dict()
    tarefa_data["user_id"] = current_user.id
    return crud.create_tarefa(db, tarefa_data)

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