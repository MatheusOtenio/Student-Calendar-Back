from database import engine
import models

def init_db():
    # Cria todas as tabelas definidas nos modelos
    models.Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()