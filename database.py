import logging
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

# Configuração de logging
logger = logging.getLogger("uvicorn.error")

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL não está definida nas variáveis de ambiente")
    DATABASE_URL = "sqlite:///./test.db"
    logger.warning(f"Usando banco de dados SQLite local: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={} if DATABASE_URL.startswith("postgresql") else {"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except exc.OperationalError as e:
        logger.error(f"Erro de conexão com o banco de dados: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Serviço de banco de dados indisponível, tente novamente mais tarde"
        )
    except exc.SQLAlchemyError as e:
        logger.error(f"Erro de banco de dados: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro interno do servidor ao processar a requisição"
        )
    finally:
        db.close()

# Função para verificar a conexão com o banco de dados
def check_database_connection():
    try:
        with SessionLocal() as db:
            db.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error(f"Falha na conexão com o banco de dados: {str(e)}")
        return False