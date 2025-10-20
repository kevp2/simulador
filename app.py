# app.py
import streamlit as st
import json
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
ADMIN_EMAIL = "kevin.172062@fmm.org.br"

# ---------- TÓPICOS ---------- (resumido aqui, substituir pelo conteúdo completo de cada tópico com 10 questões)
TOPICOS = {
    "Segurança no trabalho": {
        "conteudo": "Conteúdo completo de Segurança no Trabalho, incluindo NR-6, NR-12 e exemplos práticos.",
        "questoes": [
            {"pergunta": "De acordo com a NR-6, qual ação correta ao identificar um EPI danificado?",
             "opcoes": ["Consertar sozinho", "Comunicar e aguardar substituição", "Continuar sem EPI"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Consertar sozinho pode colocar sua vida em risco.",
                 "Correto: Comunicar imediatamente e aguardar substituição é o correto.",
                 "Errado: Continuar sem EPI viola normas de segurança."]
            },
            # Adicione as 9 questões restantes aqui...
        ]
    },
    "Boas práticas": {
        "conteudo": "Conteúdo completo sobre Boas Práticas Industriais e ética operacional.",
        "questoes": [
            # 10 questões completas
        ]
    },
    "Compliance": {
        "conteudo": "Conteúdo completo sobre Compliance Industrial e cumprimento das NRs.",
        "questoes": [
            # 10 questões completas
        ]
    },
    "Assédio moral e sexual": {
        "conteudo": "Conteúdo completo sobre assédio moral e sexual, prevenção e conduta ética.",
        "questoes": [
            # 10 questões completas
        ]
    },
    "Normas Regulamentadoras": {
        "conteudo": "Conteúdo completo sobre NRs (NR-6, NR-12, NR-26, NR-17) interpretadas eticamente.",
        "questoes": [
            # 10 questões completas
        ]
    }
}

# ---------- FUNÇÕES ----------
def save_user_data(user_email, payload):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    existing = {}
    if path.exists():
        existing = json.loads(path.read_text(encoding='utf-8'))
    existing.setdefault("history", []).append(payload)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')

def get_user_data(user_email):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))

def initialize_session():
    if "results" not in st.session_state:
        st.session_state["results"] = {}
    if "feedbacks" not in st.session_state:
        st.session_state["feedbacks"] = {}

# ---------- LOGIN ----------
def login_screen():
    st.header("Simulador Ético Industrial — Login")
    name = st.text_input("Nome")
    email = st.text_input("Email")
    if st.button("Entrar"):
        if email:
            st.session_state["user"] = {"name": name, "email": email}
            st.success(f"Olá, {name}! Login efetuado.")
            st.experimental_rerun()
            return
        else:
            st.error("Informe seu e-mail para continuar.")
    # Botão logout aparece se já houver sessão
    if st.session_state.get("user"):
        if st.button("Sair"):
            st.session_state.pop("user")
            st.success("Logout realizado.")
            st.experimental_rerun()
            return

# ---------- TELA DE TÓPICOS ----------
def show_topics():
    st.header("Tópicos")
    topico_selecionado = st.selectbox("Escolha um tópico:", list(TOPICOS.keys()))
    topico = TOPICOS[topico_selecionado]
    st.subheader("Conteúdo")
    st.write(topico["conteudo"])

    respostas_usuario = []
    st.subheader("Questões")
    for idx, q in enumerate(topico["questoes"]):
        resposta = st.radio(f"{idx+1}. {q['pergunta']}", q["opcoes"], key=f"{topico_selecionado}_{idx}")
        respostas_usuario.append(resposta)

    if st.button("Enviar respostas"):
        acertos = 0
        detalhes = []
        for idx, q in enumerate(topico["questoes"]):
            correta = q["opcoes"][q["resposta"]]
            explicacao = q["explicacao"]
            resposta_usuario = respostas_usuario[idx]
            acerto = (resposta_usuario == correta)
            acertos += acerto
            detalhes.append({
                "pergunta": q["pergunta"],
                "resposta_usuario": resposta_usuario,
                "correta": correta,
                "explicacao": explicacao
            })
        st.success(f"Você acertou {acertos}/{len(topico['questoes'])} questões.")
        st.write("Detalhes por questão:")
        for d in detalhes:
            st.markdown(f"**{d['pergunta']}**")
            st.write(f"Sua resposta: {d['resposta_usuario']}")
            st.write(f"Correta: {d['correta']}")
            for e in d["explicacao"]:
                st.write(f"- {e}")
        feedback = st.text_area("Deixe seu feedback sobre o que aprendeu:")
        save_user_data(st.session_state["user"]["email"], {
            "topico": topico_selecionado,
            "detalhes": detalhes,
            "acertos": acertos,
            "feedback": feedback
        })

# ---------- TELA DE ADMIN ----------
def admin_panel():
    st.header("Painel de Administração")
    st.write("Visualização de desempenho e exportação de dados.")

    arquivos = list(DATA_DIR.glob("*.json"))
    for arquivo in arquivos:
        email_usuario = arquivo.stem.replace("_at_", "@")
        st.subheader(f"Usuário: {email_usuario}")
        data = json.loads(arquivo.read_text(encoding='utf-8'))
        df = pd.DataFrame(data.get("history", []))
        if not df.empty:
            st.write(df[["topico","acertos","feedback"]])
            # Gráfico de pizza
            for idx, row in df.iterrows():
                st.write(f"Tópico: {row['topico']}")
                plt.figure()
                plt.pie([row['acertos'], len(TOPICOS[row['topico']]['questoes']) - row['acertos']],
                        labels=["Acertos", "Erros"], autopct="%1.1f%%", colors=["green","red"])
                st.pyplot(plt)
    if st.button("Exportar CSV de todos os usuários"):
        combined = []
        for arquivo in arquivos:
            email_usuario = arquivo.stem.replace("_at_", "@")
            data = json.loads(arquivo.read_text(encoding='utf-8'))
            for h in data.get("history", []):
                h["email"] = email_usuario
                combined.append(h)
        df_all = pd.DataFrame(combined)
        csv_path = DATA_DIR / "export_all_users.csv"
        df_all.to_csv(csv_path, index=False)
        st.success(f"CSV exportado em: {csv_path}")

# ---------- MAIN ----------
def main():
    initialize_session()
    if "user" not in st.session_state:
        login_screen()
        return
    st.sidebar.write(f"Logado como: {st.session_state['user']['email']}")
    if st.session_state["user"]["email"] == ADMIN_EMAIL:
        painel_opcoes = ["Tópicos", "Admin"]
    else:
        painel_opcoes = ["Tópicos"]
    opcao = st.sidebar.selectbox("Menu", painel_opcoes)
    if st.sidebar.button("Logout"):
        st.session_state.pop("user")
        st.experimental_rerun()
        return
    if opcao == "Tópicos":
        show_topics()
    elif opcao == "Admin":
        admin_panel()

if __name__ == "__main__":
    main()
