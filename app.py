# app.py
import streamlit as st
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# ---------- CONFIG ----------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

TOPICOS = {
    "Segurança no trabalho": {
        "conteudo": (
            "Segurança no trabalho engloba o uso correto de EPIs, bloqueio e travamento de máquinas, "
            "identificação de riscos e comunicação. Exemplos reais: procedimentos de bloqueio antes da manutenção, "
            "uso obrigatório de EPI em áreas de fundição e inspeções periódicas."
        ),
        "questoes": [
            {
                "pergunta": "Antes de realizar manutenção em uma prensa, qual a atitude correta?",
                "opcoes": ["Continuar operando e ficar atento", "Aplicar procedimento de bloqueio/etiquetagem", "Pedir a outro colega para usar a máquina"],
                "resposta": 1
            },
            {
                "pergunta": "Qual o papel do EPI?",
                "opcoes": ["Substituir treinamento", "Reduzir exposição a riscos", "Aumentar produtividade automaticamente"],
                "resposta": 1
            },
            {
                "pergunta": "Se você identificar um risco imediato, você deve:",
                "opcoes": ["Ignorar para não atrasar produção", "Registrar e comunicar ao líder e isolar a área", "Tentar consertar sozinho sem parar a linha"],
                "resposta": 1
            },
        ],
    },
    "Compliance": {
        "conteudo": (
            "Compliance refere-se ao cumprimento de leis, normas e políticas internas. Inclui reporte de condutas impróprias, "
            "evitar conflito de interesse e seguir os canais disponíveis para denúncias."
        ),
        "questoes": [
            {
                "pergunta": "O que é compliance?",
                "opcoes": ["Conjunto de práticas para cumprir leis e políticas", "Somente o RH fiscaliza", "Só documento contábil"],
                "resposta": 0
            },
            {
                "pergunta": "Se souber de conduta antiética, eu devo:",
                "opcoes": ["Não me envolver", "Reportar pelos canais da empresa", "Divulgar nas redes sociais"],
                "resposta": 1
            },
            {
                "pergunta": "Conflito de interesse deve ser:",
                "opcoes": ["Oculto", "Gerenciado e reportado", "Incentivado"],
                "resposta": 1
            },
        ],
    },
    "Boas práticas no trabalho": {
        "conteudo": (
            "Boas práticas incluem organização 5S, comunicação clara, respeito a procedimentos, troca segura de turno e "
            "reportar problemas imediatamente. Melhora qualidade e segurança."
        ),
        "questoes": [
            {
                "pergunta": "5S ajuda a:",
                "opcoes": ["Organização e eficiência", "Aumentar risco", "Substituir manutenção"],
                "resposta": 0
            },
            {
                "pergunta": "Uma boa prática na troca de turno é:",
                "opcoes": ["Não falar nada", "Fazer passagem de turno estruturada", "Só deixar bilhetes"],
                "resposta": 1
            },
            {
                "pergunta": "Comunicação clara evita:",
                "opcoes": ["Atrasos e acidentes", "Segurança", "Qualidade"],
                "resposta": 0
            },
        ],
    },
    "Assédio moral e sexual": {
        "conteudo": (
            "Assédio é qualquer conduta que ofenda a dignidade da pessoa. A empresa deve prevenir, acolher vítimas e aplicar medidas. "
            "Denuncie por canais internos; proteger a vítima é prioridade."
        ),
        "questoes": [
            {
                "pergunta": "Assédio moral é:",
                "opcoes": ["Brincadeira entre amigos", "Atitude repetitiva que humilha a pessoa", "Só físico"],
                "resposta": 1
            },
            {
                "pergunta": "Se você presenciar assédio, você deve:",
                "opcoes": ["Ignorar", "Notificar e apoiar a vítima", "Compartilhar nas redes sociais"],
                "resposta": 1
            },
            {
                "pergunta": "Assédio sexual é crime quando:",
                "opcoes": ["Só se houver agressão física", "Qualquer comportamento sexual indesejado", "Nunca é crime"],
                "resposta": 1
            },
        ],
    },
    "Normas Regulamentadoras": {
        "conteudo": (
            "Normas Regulamentadoras (NRs) definem requisitos para SST (saúde e segurança). Exemplos: NR-12 (máquinas), NR-6 (EPI). "
            "Seguir NRs é obrigatório e reduz riscos legais e acidentes."
        ),
        "questoes": [
            {
                "pergunta": "A NR-6 trata de:",
                "opcoes": ["Máquinas", "EPI", "Ergonomia"],
                "resposta": 1
            },
            {
                "pergunta": "NR-12 é relacionada a:",
                "opcoes": ["Máquinas e segurança", "Ambiental", "Financeira"],
                "resposta": 0
            },
            {
                "pergunta": "Cumprir NRs é:",
                "opcoes": ["Opcional", "Obrigatório", "Somente para gestores"],
                "resposta": 1
            },
        ],
    },
}

# ---------- HELPERS ----------
def save_user_data(user_email, payload):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text())
        except Exception:
            existing = {}
    existing.setdefault("history", []).append(payload)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False))

def get_aggregate_for_user(user_email):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        return data
    except Exception:
        return {}

def initialize_session():
    if "results" not in st.session_state:
        st.session_state["results"] = {}  # topic -> list of scores (0..100)
    if "feedbacks" not in st.session_state:
        st.session_state["feedbacks"] = {}  # topic -> list of feedbacks

# ---------- AUTH (Google via Streamlit OR fallback) ----------
def login_screen():
    st.header("Simulador Ético Industrial — Acesso")
    st.write("Faça login para iniciar o treinamento.")
    # If Streamlit auth is configured, use it:
    if st.secrets.get("auth", None):
        st.button("Entrar com Google", on_click=st.login)
        st.caption("Se o Google aparecer e não redirecionar, verifique os redirect URIs nas credenciais do Google Cloud.")
    else:
        st.info("Login Google não configurado. Use o login simulado abaixo enquanto configura as credenciais.")
        name = st.text_input("Nome (simulado)", key="mock_name")
        email = st.text_input("Email (simulado)", key="mock_email")
        if st.button("Entrar (simulado)"):
            if email:
                # criar user simulado
                st.session_state["user"] = {"name": name or email.split("@")[0], "email": email}
                st.experimental_rerun()
            else:
                st.error("Informe um email para o login simulado.")

def get_logged_user():
    # If Streamlit builtin OAuth provides st.user:
    if hasattr(st, "user") and st.user is not None and getattr(st.user, "is_logged_in", False):
        # st.user tem atributos; algumas versões retornam dict-like
        try:
            # st.user pode ser um object com .name e .email
            name = getattr(st.user, "name", None) or st.user.get("name")
            email = getattr(st.user, "email", None) or st.user.get("email")
            return {"name": name, "email": email}
        except Exception:
            # fallback
            return None
    # fallback para login simulado via session_state
    if st.session_state.get("user"):
        return st.session_state["user"]
    return None

# ---------- UI PAGES ----------
def page_topicos(user):
    st.title("TÓPICOS — Simulador Ético Industrial")
    st.sidebar.header(f"Olá, {user['name']}")
    st.sidebar.button("Sair", on_click=logout)
    tab = st.selectbox("Escolha um tópico para estudar", list(TOPICOS.keys()))
    info = TOPICOS[tab]
    st.subheader(tab)
    st.write(info["conteudo"])

    st.markdown("---")
    st.subheader("Quiz — Verifique sua compreensão")
    respostas = []
    perguntas = info["questoes"]
    cols = st.columns(1)
    with st.form(key=f"form_{tab}"):
        selections = []
        for i, q in enumerate(perguntas):
            sel = st.radio(f"{i+1}. {q['pergunta']}", q["opcoes"], key=f"{tab}_q{i}")
            selections.append(sel)
        submitted = st.form_submit_button("Enviar respostas")
        if submitted:
            score = 0
            for i, q in enumerate(perguntas):
                escolha = selections[i]
                correto = q["opcoes"][q["resposta"]]
                if escolha == correto:
                    score += 1
            pct = int((score / len(perguntas)) * 100)
            st.success(f"Você acertou {score} de {len(perguntas)} — {pct}%")
            # guardar no session_state
            st.session_state["results"].setdefault(tab, []).append({"score": pct, "time": datetime.now().isoformat()})
            # persistir no arquivo do usuário (opcional)
            save_user_data(user["email"], {"topic": tab, "score": pct, "time": datetime.now().isoformat()})
            # pedir feedback
            feedback = st.text_area("Conte aqui o que aprendeu neste tópico (feedback):", key=f"fb_{tab}")
            if st.button("Enviar feedback", key=f"sendfb_{tab}"):
                st.success("Obrigado pelo feedback!")
                st.session_state["feedbacks"].setdefault(tab, []).append({"text": feedback, "time": datetime.now().isoformat()})
                # salvar também
                save_user_data(user["email"], {"topic": tab, "feedback": feedback, "time": datetime.now().isoformat()})

def page_dados(user):
    st.title("DADOS — Evolução por tópico")
    st.sidebar.header(f"Olá, {user['name']}")
    st.sidebar.button("Sair", on_click=logout)

    # coletar dados do session_state e do arquivo se existir
    agg = get_aggregate_for_user(user["email"])
    # montar df a partir de st.session_state results para mostrar algo imediato
    rows = []
    for topic, entries in st.session_state.get("results", {}).items():
        # entries é lista de dicts
        for e in entries:
            rows.append({"topic": topic, "score": e["score"], "time": e["time"]})
    # também adicionar arquivo salvo
    if agg.get("history"):
        for e in agg["history"]:
            rows.append({"topic": e.get("topic", "unknown"), "score": e.get("score", None), "time": e.get("time", None), "feedback": e.get("feedback", None)})

    if not rows:
        st.info("Sem dados de desempenho ainda. Faça um quiz em um tópico para gerar dados.")
        return

    df = pd.DataFrame(rows)
    st.write("Tabela de registros (últimos resultados):")
    st.dataframe(df.sort_values("time", ascending=False).head(50))

    st.markdown("---")
    st.subheader("Gráfico: média por tópico")
    # calcular média
    df_scores = df.dropna(subset=["score"])
    if df_scores.empty:
        st.info("Ainda não há pontuações registradas.")
        return
    avg = df_scores.groupby("topic")["score"].mean().reset_index()
    # plot com matplotlib (compatível)
    fig, ax = plt.subplots()
    ax.bar(avg["topic"], avg["score"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Média de acerto (%)")
    ax.set_xlabel("Tópico")
    ax.set_title("Evolução média por tópico")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

def logout():
    # logout do st (quando autenticação nativa está ativa)
    try:
        if hasattr(st, "logout"):
            st.logout()
    except Exception:
        pass
    # limpar session
    for k in list(st.session_state.keys()):
        if k not in ("results", "feedbacks"):
            try:
                del st.session_state[k]
            except Exception:
                pass
    st.experimental_rerun()

# ---------- MAIN ----------
def main():
    st.set_page_config(page_title="Simulador Ético Industrial", layout="wide")
    initialize_session()
    st.sidebar.title("Simulador Ético Industrial")
    # autenticação
    user = get_logged_user()
    if not user:
        login_screen()
        return

    # quando logado:
    st.sidebar.write(f"Usuário: {user['name']}")
    page = st.sidebar.selectbox("Navegação", ["Tópicos", "Dados", "Sobre"])
    if page == "Tópicos":
        page_topicos(user)
    elif page == "Dados":
        page_dados(user)
    else:
        st.title("Sobre")
        st.write(
            "Simulador para treinar comportamentos e ética em ambiente industrial.\n\n"
            "Tópicos disponíveis: " + ", ".join(TOPICOS.keys())
        )
        st.write("Se o login Google estiver configurado, use o botão de logout na barra lateral.")

if __name__ == "__main__":
    main()
