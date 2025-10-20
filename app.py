# app.py
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
ADMIN_EMAIL = "kevin.172062@fmm.org.br"

# ---------- TÓPICOS (exemplo simplificado, complete com 10 questões cada) ----------
TOPICOS = {
    "Segurança no trabalho": {
        "conteudo": (
            "A segurança no trabalho é imperativo legal e ético. "
            "NR-6 exige uso de EPIs. NR-12 estabelece requisitos de proteção de máquinas. "
            "Reportar riscos, usar EPIs corretamente e seguir bloqueios são práticas obrigatórias."
        ),
        "questoes": [
            {
                "pergunta": "De acordo com a NR-6, qual ação correta ao identificar um EPI danificado?",
                "opcoes": ["Consertar sozinho", "Comunicar e aguardar substituição", "Continuar sem EPI"],
                "resposta": 1,
                "explicacao": [
                    "Errado: Consertar sozinho pode colocar sua vida em risco.",
                    "Correto: Comunicar imediatamente e aguardar substituição.",
                    "Errado: Continuar sem EPI viola normas de segurança."]
            },
            {
                "pergunta": "Participar de treinamentos de segurança é:",
                "opcoes": ["Opcional", "Obrigatório e ético", "Perda de tempo"],
                "resposta": 1,
                "explicacao": [
                    "Errado: Não é opcional.",
                    "Correto: Treinamentos são obrigatórios e reforçam ética.",
                    "Errado: Não é perda de tempo."]
            }
        ]
    },
    "Boas práticas": {
        "conteudo": (
            "Boas práticas industriais envolvem 5S, checklists, reportar não conformidades, "
            "manter áreas limpas e organizar materiais para segurança e eficiência."
        ),
        "questoes": [
            # Adicione 10 questões completas aqui
        ]
    },
    "Compliance": {
        "conteudo": (
            "Compliance industrial garante atuação dentro de normas legais, éticas e regulamentares. "
            "Inclui código de conduta, prevenção de fraudes e cumprimento das NRs."
        ),
        "questoes": [
            # Adicione 10 questões completas aqui
        ]
    },
    "Assédio moral e sexual": {
        "conteudo": (
            "Assédio moral: humilhação, intimidação ou tratamento desigual repetido. "
            "Assédio sexual: comentários, gestos ou convites indesejados de cunho sexual. "
            "Reportar qualquer situação de assédio é obrigação ética e legal."
        ),
        "questoes": [
            # Adicione 10 questões completas aqui
        ]
    },
    "Normas Regulamentadoras": {
        "conteudo": (
            "NRs definem obrigações legais e práticas de segurança. Exemplos: NR-6 (EPI), NR-12 (máquinas), NR-26 (sinalização), NR-17 (ergonomia). "
            "Cumprir NRs garante ética, proteção física e legalidade."
        ),
        "questoes": [
            # Adicione 10 questões completas aqui
        ]
    },
}

# ---------- FUNÇÕES DE DADOS ----------
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
        return {"history": []}
    return json.loads(path.read_text(encoding='utf-8'))

# ---------- LOGIN ----------
def login_screen():
    st.header("Simulador Ético Industrial — Login")
    # Logout se já estiver logado
    if st.session_state.get("user"):
        st.write(f"Logado como: {st.session_state['user']['email']}")
        if st.button("Sair"):
            st.session_state.pop("user")
            st.experimental_rerun()
        return  # Evita continuar execução
    # Login
    name = st.text_input("Nome")
    email = st.text_input("Email")
    if st.button("Entrar"):
        if email:
            st.session_state["user"] = {"name": name, "email": email}
            st.success(f"Olá, {name}! Login efetuado.")
            st.experimental_rerun()
        else:
            st.error("Informe seu e-mail para continuar.")

# ---------- TELA DE TÓPICOS ----------
def topico_screen():
    st.header("Escolha um Tópico")
    topico_escolhido = st.selectbox("Tópicos disponíveis", list(TOPICOS.keys()))
    conteudo = TOPICOS[topico_escolhido]["conteudo"]
    st.subheader("Conteúdo")
    st.write(conteudo)
    st.subheader("Questionário")
    respostas_usuario = []
    for i, q in enumerate(TOPICOS[topico_escolhido]["questoes"]):
        st.write(f"**{i+1}. {q['pergunta']}**")
        escolha = st.radio("", q["opcoes"], key=f"{topico_escolhido}_{i}")
        respostas_usuario.append(escolha)
    if st.button("Enviar Respostas", key=f"enviar_{topico_escolhido}"):
        acertos = 0
        detalhes = []
        for i, q in enumerate(TOPICOS[topico_escolhido]["questoes"]):
            idx_escolha = TOPICOS[topico_escolhido]["questoes"][i]["opcoes"].index(respostas_usuario[i])
            if idx_escolha == q["resposta"]:
                acertos += 1
            detalhes.append({
                "pergunta": q["pergunta"],
                "resposta_usuario": respostas_usuario[i],
                "correto": q["opcoes"][q["resposta"]],
                "explicacao": q["explicacao"][idx_escolha]
            })
        st.write(f"Você acertou {acertos} de {len(TOPICOS[topico_escolhido]['questoes'])}")
        for d in detalhes:
            st.write(f"- {d['pergunta']}")
            st.write(f"  - Sua resposta: {d['resposta_usuario']}")
            st.write(f"  - Correta: {d['correto']}")
            st.write(f"  - Explicação: {d['explicacao']}")
        feedback = st.text_area("Feedback: O que você aprendeu?")
        payload = {
            "topico": topico_escolhido,
            "detalhes": detalhes,
            "feedback": feedback,
            "timestamp": str(datetime.now())
        }
        save_user_data(st.session_state["user"]["email"], payload)
        st.success("Dados salvos!")

# ---------- TELA DE ADMIN ----------
def admin_screen():
    st.header("Administração — Exportar Dados")
    if st.session_state["user"]["email"] != ADMIN_EMAIL:
        st.error("Acesso negado.")
        return
    arquivos = list(DATA_DIR.glob("*.json"))
    if not arquivos:
        st.info("Nenhum dado encontrado.")
        return
    for arquivo in arquivos:
        data = json.loads(arquivo.read_text(encoding="utf-8"))
        st.write(f"Usuário: {arquivo.stem.replace('_at_','@')}")
        for h in data.get("history", []):
            st.write(h)
    # Exportar CSV
    if st.button("Exportar todos os dados para CSV"):
        import pandas as pd
        all_data = []
        for arquivo in arquivos:
            data = json.loads(arquivo.read_text(encoding="utf-8"))
            email = arquivo.stem.replace("_at_", "@")
            for h in data.get("history", []):
                for d in h["detalhes"]:
                    all_data.append({
                        "email": email,
                        "topico": h["topico"],
                        "pergunta": d["pergunta"],
                        "resposta_usuario": d["resposta_usuario"],
                        "resposta_correta": d["correto"],
                        "explicacao": d["explicacao"],
                        "feedback": h["feedback"],
                        "timestamp": h["timestamp"]
                    })
        df = pd.DataFrame(all_data)
        csv_path = DATA_DIR / "export_dados.csv"
        df.to_csv(csv_path, index=False)
        st.success(f"CSV salvo em {csv_path}")

# ---------- GRAFICOS DE DESEMPENHO ----------
def performance_screen():
    st.header("Desempenho do usuário")
    user_email = st.session_state["user"]["email"]
    data = get_user_data(user_email)
    if not data["history"]:
        st.info("Nenhum dado disponível.")
        return
    for topico in TOPICOS.keys():
        acertos = 0
        erros = 0
        for h in data["history"]:
            if h["topico"] == topico:
                for d in h["detalhes"]:
                    if d["resposta_usuario"] == d["correto"]:
                        acertos += 1
                    else:
                        erros += 1
        if acertos + erros > 0:
            st.write(f"**{topico}**")
            fig, ax = plt.subplots()
            ax.pie([acertos, erros], labels=["Acertos", "Erros"], autopct="%1.1f%%", colors=["green","red"])
            st.pyplot(fig)

# ---------- MAIN ----------
def main():
    if "user" not in st.session_state:
        login_screen()
        return
    menu = ["Tópicos", "Desempenho", "Administração"]
    escolha = st.sidebar.selectbox("Menu", menu)
    if escolha == "Tópicos":
        topico_screen()
    elif escolha == "Desempenho":
        performance_screen()
    elif escolha == "Administração":
        admin_screen()

if __name__ == "__main__":
    main()
