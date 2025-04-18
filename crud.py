from sqlalchemy.orm import Session
from models import Tarefa, Cronograma, User
from auth import get_password_hash, verify_password

# Funções CRUD para usuários
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Função authenticate_user foi movida para auth.py para evitar duplicação

def create_user(db: Session, user_data):
    try:
        # Verifica se user_data é um dicionário ou um objeto Pydantic
        if hasattr(user_data, "dict"):
            password = user_data.password
            user_dict = user_data.dict()
            del user_dict["password"]  # Remove senha em texto plano
        else:
            password = user_data["password"]
            user_dict = user_data.copy()
            user_dict.pop("password", None)  # Remove senha em texto plano
            
        hashed_password = get_password_hash(password)
        db_user = User(**user_dict, hashed_password=hashed_password)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def get_tarefas(db: Session, user_id: int = None):
    if user_id:
        return db.query(Tarefa).filter(Tarefa.user_id == user_id).all()
    return db.query(Tarefa).all()

def create_tarefa(db: Session, tarefa_data: dict):
    nova_tarefa = Tarefa(**tarefa_data)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

def update_tarefa(db: Session, tarefa_id: int, tarefa_data: dict):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        return None
    for key, value in tarefa_data.items():
        setattr(db_tarefa, key, value)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def delete_tarefa(db: Session, tarefa_id: int):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        return None
    db.delete(db_tarefa)
    db.commit()
    return db_tarefa

def get_cronogramas(db: Session, user_id: int = None):
    if user_id:
        return db.query(Cronograma).filter(Cronograma.user_id == user_id).all()
    return db.query(Cronograma).all()

def create_cronograma(db: Session, cronograma_data: dict):
    novo_cronograma = Cronograma(**cronograma_data)
    db.add(novo_cronograma)
    db.commit()
    db.refresh(novo_cronograma)
    return novo_cronograma