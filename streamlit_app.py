import streamlit as st
import requests
from datetime import datetime, date

# Configuração da URL base da API
# Usar variável de ambiente ou URL de produção do Render
import os
API_URL = os.getenv("API_URL", "https://student-calendar-back.onrender.com")

# Configuração da página Streamlit
st.set_page_config(page_title="Calendário Estudantil", layout="wide")
st.title("Calendário Estudantil")

# Função para fazer login
def login(username, password):
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Interface de login
def show_login():
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            result = login(username, password)
            if result:
                st.session_state["token"] = result["access_token"]
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

# Página principal
def main_page():
    st.write("Bem-vindo ao seu Calendário Estudantil!")
    
    # Adicionar nova tarefa
    with st.expander("Adicionar Nova Tarefa"):
        with st.form("nova_tarefa"):
            nome = st.text_input("Nome da Tarefa")
            descricao = st.text_area("Descrição")
            data_limite = st.date_input("Data Limite")
            hora_limite = st.time_input("Hora Limite")
            submit = st.form_submit_button("Adicionar Tarefa")
            
            if submit:
                data_hora = datetime.combine(data_limite, hora_limite)
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.post(
                    f"{API_URL}/tarefas",
                    headers=headers,
                    json={
                        "nome": nome,
                        "descricao": descricao,
                        "data_limite": data_hora.isoformat()
                    }
                )
                if response.status_code == 200:
                    st.success("Tarefa adicionada com sucesso!")
                else:
                    st.error("Erro ao adicionar tarefa")
    
    # Listar tarefas
    st.subheader("Suas Tarefas")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/tarefas", headers=headers)
    
    if response.status_code == 200:
        tarefas = response.json()
        for tarefa in tarefas:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{tarefa['nome']}**")
                    st.write(tarefa['descricao'])
                with col2:
                    data_limite = datetime.fromisoformat(tarefa['data_limite'])
                    st.write(f"Data Limite: {data_limite.strftime('%d/%m/%Y %H:%M')}")

# Gerenciamento da sessão
if "token" not in st.session_state:
    show_login()
else:
    main_page()