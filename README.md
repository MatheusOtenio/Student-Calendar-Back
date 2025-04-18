# Student Calendar Backend

API backend para o aplicativo Student Calendar, desenvolvido com FastAPI e PostgreSQL.

## Requisitos

- Python 3.8+
- PostgreSQL

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/MatheusOtenio/Student-Calendar-Back.git
   cd Student-Calendar-Back
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
   ```

5. Inicie o servidor de desenvolvimento:
   ```
   uvicorn main:app --reload
   ```

## Deploy no Render

1. Crie uma conta no [Render](https://render.com/)

2. Crie um novo Web Service e conecte ao repositório GitHub

3. Configure o serviço:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. Adicione a variável de ambiente `DATABASE_URL` apontando para seu banco de dados PostgreSQL

5. Clique em "Create Web Service"

## Estrutura do Projeto

- `main.py`: Configuração da API FastAPI e definição de endpoints
- `models.py`: Modelos SQLAlchemy para o banco de dados
- `database.py`: Configuração da conexão com o banco de dados
- `crud.py`: Funções para operações CRUD no banco de dados

## API Endpoints

### Tarefas
- `GET /tarefas`: Lista todas as tarefas
- `POST /tarefas`: Cria uma nova tarefa
- `PUT /tarefas/{tarefa_id}`: Atualiza uma tarefa existente
- `DELETE /tarefas/{tarefa_id}`: Remove uma tarefa

### Cronogramas
- `GET /cronogramas`: Lista todos os cronogramas
- `POST /cronogramas`: Cria um novo cronograma