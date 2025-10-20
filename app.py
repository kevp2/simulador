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

# ---------- TOPICOS COMPLETOS COM 10 QUESTÕES CADA ----------
TOPICOS = {
    "Segurança no trabalho": {
        "conteudo": (
            "A segurança no trabalho é um imperativo legal e ético na indústria. "
            "A NR-6 determina a obrigatoriedade do fornecimento, uso e conservação dos EPIs "
            "quando os riscos não podem ser eliminados por medidas coletivas. "
            "A NR-12 estabelece requisitos de projeto, proteção e manutenção de máquinas, "
            "incluindo dispositivos de bloqueio (lockout/tagout), proteções físicas e intertravamentos. "
            "Programas de controle de riscos (identificação, avaliação e mitigação) são fundamentais para redução de exposições. "
            "No dia a dia do operador, agir conforme procedimentos de bloqueio, usar EPIs, reportar riscos e participar de treinamentos "
            "são práticas que unem conformidade legal e responsabilidade ética."
        ),
        "questoes": [
            {"pergunta": "De acordo com a NR-6, qual a ação correta ao identificar um EPI danificado antes do turno?",
             "opcoes": ["Consertar sozinho e usar normalmente", "Comunicar e aguardar substituição", "Continuar sem EPI se for rápido"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Consertar sozinho pode colocar sua vida em risco.",
                 "Correto: Comunicar imediatamente e aguardar substituição é o procedimento correto e ético.",
                 "Errado: Continuar sem EPI é uma violação das normas de segurança e ética."]
            },
            {"pergunta": "Ao operar uma máquina sem proteção adequada, o operador está:",
             "opcoes": ["Cumprindo a NR-12", "Violando normas e ética", "Aumentando produtividade legalmente"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Cumprir a NR-12 exige proteção.",
                 "Correto: Operar sem proteção é violar norma e ética.",
                 "Errado: Não é legal nem seguro."]
            },
            {"pergunta": "Participar de treinamentos de segurança é:",
             "opcoes": ["Opcional", "Obrigatório e ético", "Perda de tempo"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é opcional.",
                 "Correto: Treinamentos são obrigatórios e reforçam ética.",
                 "Errado: Não é perda de tempo."]
            },
            {"pergunta": "O que deve ser feito ao identificar risco de acidente?",
             "opcoes": ["Ignorar se não afetar você", "Reportar imediatamente", "Apenas observar"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Ignorar é antiético.",
                 "Correto: Reportar imediatamente é procedimento correto.",
                 "Errado: Apenas observar não previne acidente."]
            },
            {"pergunta": "Bloquear uma máquina durante manutenção é:",
             "opcoes": ["Irrelevante", "Exigência da NR-12", "Opcional se estiver com pressa"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é irrelevante.",
                 "Correto: Bloqueio é exigência da NR-12.",
                 "Errado: Nunca opcional."]
            },
            {"pergunta": "Usar EPI de forma inadequada pode resultar em:",
             "opcoes": ["Acidentes e penalidades", "Nada acontece", "Recomendação de produção"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Uso inadequado pode gerar acidentes e punições.",
                 "Errado: Algo pode acontecer sim.",
                 "Errado: Não é recomendação de produção."]
            },
            {"pergunta": "NR-12 estabelece que proteções em máquinas devem ser:",
             "opcoes": ["Sempre removíveis para agilizar operação", "Fixas e seguras", "Ignoradas se operador for experiente"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Nunca removíveis apenas para agilizar.",
                 "Correto: Proteções devem ser fixas e seguras.",
                 "Errado: Não devem ser ignoradas."]
            },
            {"pergunta": "Se houver dúvida sobre segurança, o operador deve:",
             "opcoes": ["Adivinhar procedimento", "Consultar manual ou supervisor", "Ignorar o risco"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Adivinhar é inseguro.",
                 "Correto: Consultar manual ou supervisor é seguro.",
                 "Errado: Ignorar risco é antiético."]
            },
            {"pergunta": "Cumprir procedimentos de bloqueio é:",
             "opcoes": ["Opcional para operadores experientes", "Obrigatório e ético", "Desnecessário"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Nunca opcional.",
                 "Correto: Cumprimento é obrigatório e ético.",
                 "Errado: Não é desnecessário."]
            },
            {"pergunta": "Reportar quase acidentes contribui para:",
             "opcoes": ["Prevenção de futuros acidentes", "Nada", "Somente punição de colegas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Ajuda a prevenir acidentes futuros.",
                 "Errado: Tem impacto real.",
                 "Errado: Não é para punir colegas."]
            }
        ]
    },
    # -------------------- OUTROS TÓPICOS (Boas Práticas, Compliance, Assédio, Normas) --------------------
    # Aqui você pode incluir os outros tópicos com 10 questões cada, seguindo o mesmo modelo de Segurança
}

# ---------- FUNÇÕES DE DADOS ----------
def save_user_data(user_email, topico, questao, acertou, feedback):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    if path.exists():
        data = json.loads(path.read_text(encoding='utf-8'))
    else:
        data = {}
    data.setdefault("respostas", []).append({
        "topico": topico,
        "questao": questao,
        "acertou": acertou,
        "feedback": feedback
    })
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

def load_user_data(user_email):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}

# ---------- LOGIN ----------
def login_screen():
    st.header("Simulador Ético Industrial — Login")
    if "user" not in st.session_state:
        name = st.text_input("Nome")
        email = st.text_input("Email")
        if st.button("Entrar"):
            if email:
                st.session_state["user"] = {"name": name, "email": email}
                st.success(f"Olá, {name}! Login efetuado.")
            else:
                st.error("Informe seu e-mail para continuar.")
        return False
    else:
        st.write(f"Logado como: **{st.session_state['user']['name']} ({st.session_state['user']['email']})**")
        if st.button("Sair"):
            st.session_state.pop("user")
            st.success("Logout realizado.")
        return True

# ---------- TELA DE TÓPICOS ----------
def topico_screen():
    st.header("Tópicos de Treinamento")
    topico_escolhido = st.selectbox("Escolha o tópico", list(TOPICOS.keys()))
    info = TOPICOS[topico_escolhido]["conteudo"]
    st.markdown(f"**Conteúdo:**\n{info}")

    questoes = TOPICOS[topico_escolhido]["questoes"]
    respostas_usuario = []

    st.write("---")
    st.subheader("Responda as questões abaixo:")

    for i, q in enumerate(questoes):
        st.write(f"**{i+1}. {q['pergunta']}**")
        opcao = st.radio(f"Questão {i+1}", q["opcoes"], key=f"{topico_escolhido}_{i}")
        acertou = q["opcoes"].index(opcao) == q["resposta"]
        respostas_usuario.append(acertou)
        if st.button(f"Verificar questão {i+1}", key=f"verif_{i}"):
            st.write(f"**Sua resposta:** {opcao}")
            st.write(f"**Correto:** {q['opcoes'][q['resposta']]}")
            st.write(f"**Explicação:** {q['explicacao'][q['opcoes'].index(opcao)]}")

        # Coleta feedback
        feedback = st.text_area(f"Feedback sobre o que aprendeu na questão {i+1}:", key=f"fb_{i}")
        if st.button(f"Salvar feedback {i+1}", key=f"save_fb_{i}"):
            save_user_data(st.session_state["user"]["email"], topico_escolhido, q["pergunta"], acertou, feedback)
            st.success("Feedback salvo!")

# ---------- TELA DE DESEMPENHO ----------
def performance_screen():
    st.header("Desempenho do Usuário")
    user_email = st.session_state["user"]["email"]
    data = load_user_data(user_email)
    if not data.get("respostas"):
        st.info("Nenhuma resposta registrada ainda.")
        return

    df = pd.DataFrame(data["respostas"])
    for topico in df["topico"].unique():
        st.subheader(f"Tópico: {topico}")
        df_topico = df[df["topico"] == topico]
        acertos = df_topico["acertou"].sum()
        erros = len(df_topico) - acertos
        fig, ax = plt.subplots()
        ax.pie([acertos, erros], labels=["Acertos", "Erros"], autopct="%1.1f%%", colors=["green", "red"])
        ax.set_title(f"Desempenho em {topico}")
        st.pyplot(fig)

# ---------- TELA DE ADMINISTRAÇÃO ----------
def admin_screen():
    st.header("Administração")
    user_email = st.session_state["user"]["email"]
    if user_email != ADMIN_EMAIL:
        st.error("Acesso restrito.")
        return
    all_data = []
    for file in DATA_DIR.glob("*.json"):
        data = json.loads(file.read_text(encoding="utf-8"))
        for r in data.get("respostas", []):
            all_data.append({"usuario": file.stem, **r})
    if not all_data:
        st.info("Nenhum dado encontrado.")
        return
    df = pd.DataFrame(all_data)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Exportar CSV", csv, "dados.csv", "text/csv")

# ---------- MAIN ----------
def main():
    usuario_logado = login_screen()
    if not usuario_logado:
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
