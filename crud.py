from sqlalchemy.orm import Session
from models import Tarefa, Cronograma

def get_tarefas(db: Session):
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

def get_cronogramas(db: Session):
    return db.query(Cronograma).all()

def create_cronograma(db: Session, cronograma_data: dict):
    novo_cronograma = Cronograma(**cronograma_data)
    db.add(novo_cronograma)
    db.commit()
    db.refresh(novo_cronograma)
    return novo_cronograma