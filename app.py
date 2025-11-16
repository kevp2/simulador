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
    "Compliance": {
        "conteudo": (
            "Compliance industrial garante que todos os colaboradores atuem dentro das normas legais, regulamentares e éticas. "
            "Inclui políticas internas, código de conduta, canais de denúncia, prevenção de fraudes e cumprimento das NRs."
        ),
        "questoes": [
            {"pergunta": "O que é compliance?",
             "opcoes": ["Seguir leis e ética", "Apenas cumprir produção", "Ignorar riscos"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Compliance é seguir leis e ética.",
                 "Errado: Não é só produção.",
                 "Errado: Ignorar riscos é antiético."]
            },
            {"pergunta": "Reportar irregularidades é:",
             "opcoes": ["Obrigatório", "Opcional", "Proibido"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Reportar é obrigatório.",
                 "Errado: Não é opcional.",
                 "Errado: Não é proibido."]
            },
            {"pergunta": "Canais de denúncia servem para:",
             "opcoes": ["Garantir confidencialidade e correção de erros", "Difamar colegas", "Ignorar problemas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Servem para corrigir problemas de forma ética.",
                 "Errado: Não são para difamar.",
                 "Errado: Não devem ignorar problemas."]
            },
            {"pergunta": "Compliance melhora:",
             "opcoes": ["Ética e segurança", "Produção somente", "Nada"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Melhora ética, segurança e confiabilidade.",
                 "Errado: Não apenas produção.",
                 "Errado: Tem efeito real."]
            },
            {"pergunta": "Ignorar normas internas é:",
             "opcoes": ["Errado", "Aceitável", "Recomendado"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Errado e antiético.",
                 "Errado: Não é aceitável.",
                 "Errado: Nunca recomendado."]
            },
            {"pergunta": "Cumprir o código de conduta é:",
             "opcoes": ["Obrigatório e ético", "Opcional", "Só para gerência"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Todos devem cumprir.",
                 "Errado: Não é opcional.",
                 "Errado: Não é só para gerência."]
            },
            {"pergunta": "Fraudes e desvios devem ser:",
             "opcoes": ["Reportados imediatamente", "Ignorados", "Corrigidos sozinho"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Reportar imediatamente.",
                 "Errado: Ignorar é antiético.",
                 "Errado: Corrigir sozinho é inseguro."]
            },
            {"pergunta": "A NR-1 exige:",
             "opcoes": ["Cumprimento de todas as NRs", "Apenas segurança", "Não obriga nada"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-1 exige cumprimento das NRs.",
                 "Errado: Não é apenas segurança.",
                 "Errado: Obriga sim."]
            },
            {"pergunta": "Auditorias internas servem para:",
             "opcoes": ["Garantir conformidade", "Punir sem razão", "Evitar responsabilidades"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Garantem que tudo siga as normas.",
                 "Errado: Não é punir sem razão.",
                 "Errado: Não é para evitar responsabilidade."]
            },
            {"pergunta": "Compliance protege:",
             "opcoes": ["Empresa e colaboradores", "Só a diretoria", "Ninguém"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Protege todos, garantindo ética.",
                 "Errado: Não apenas diretoria.",
                 "Errado: Protege sim todos."]
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

# ---------- TELA DE TÓPICOS (NOVA VERSÃO CLEAN + QUESTÃO POR QUESTÃO) ----------
def topico_screen():
    st.title("📘 Simulador Ético Industrial")
    st.write("Selecione um tópico para iniciar o aprendizado:")

    topico_escolhido = st.selectbox("Escolha o tópico", list(TOPICOS.keys()))

    # AULA / EXPLICAÇÃO COMPLETA ANTES DAS QUESTÕES
    st.subheader(f"📖 Aula: {topico_escolhido}")
    st.info(TOPICOS[topico_escolhido]["conteudo"])

    if st.button("👉 Iniciar caderno de questões"):
        st.session_state["modo_questoes"] = True
        st.session_state["topico_atual"] = topico_escolhido
        st.session_state["questao_atual"] = 0
        st.session_state["acertos"] = 0

    # --- MODO QUESTÕES ---
    if st.session_state.get("modo_questoes", False):
        topico = st.session_state["topico_atual"]
        questoes = TOPICOS[topico]["questoes"]
        idx = st.session_state["questao_atual"]
        q = questoes[idx]

        st.write("---")
        st.subheader(f"Questão {idx+1} de {len(questoes)}")
        st.write(f"**{q['pergunta']}**")
        resposta = st.radio("Escolha a resposta:", q["opcoes"], key=f"q_{idx}")

        if st.button("Confirmar resposta"):
            acertou = q["opcoes"].index(resposta) == q["resposta"]
            if acertou:
                st.success("✔ Resposta correta!")
                st.session_state["acertos"] += 1
            else:
                st.error("❌ Resposta incorreta.")

            st.info(f"💡 Explicação: {q['explicacao'][q['opcoes'].index(resposta)]}")

            save_user_data(
                st.session_state["user"]["email"],
                topico,
                q["pergunta"],
                acertou,
                ""
            )

            if idx + 1 < len(questoes):
                if st.button("➡ Próxima questão"):
                    st.session_state["questao_atual"] += 1
            else:
                st.success("🎉 Você concluiu o questionário!")
                st.write(f"Resultado: **{st.session_state['acertos']} / {len(questoes)}** acertos")

                feedback = st.text_area("Deixe seu feedback sobre o tópico:")
                if st.button("Salvar feedback"):
                    save_user_data(
                        st.session_state["user"]["email"],
                        topico,
                        "Feedback final",
                        None,
                        feedback
                    )
                    st.success("Feedback registrado!")

                if st.button("🔁 Escolher novo tópico"):
                    st.session_state["modo_questoes"] = False
                    st.session_state["questao_atual"] = 0
                    st.session_state["acertos"] = 0
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
