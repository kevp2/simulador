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

# ---------- TOPICOS COMPLETOS ----------
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
    "Boas práticas": {
        "conteudo": (
            "Boas práticas industriais incluem organização, limpeza, padronização e comunicação eficiente. "
            "Seguir 5S, realizar checklists, reportar não conformidades, manter áreas limpas e organizar materiais garantem segurança e eficiência. "
            "Exemplo: NR-5 (CIPA) e NR-17 (ergonomia) reforçam a importância do cuidado diário com o ambiente e a postura correta do operador."
        ),
        "questoes": [
            {"pergunta": "Manter sua área limpa e organizada é:",
             "opcoes": ["Opcional", "Obrigatório e ético", "Desnecessário"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é opcional.",
                 "Correto: Organização protege a segurança e ética.",
                 "Errado: Não é desnecessário."]
            },
            {"pergunta": "Seguir os 5S significa:",
             "opcoes": ["Separar, organizar, limpar, padronizar, sustentar", "Somente limpar a área", "Apenas supervisionar colegas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: 5S é a metodologia completa.",
                 "Errado: Limpar não é suficiente.",
                 "Errado: Apenas supervisionar não é o foco."]
            },
            {"pergunta": "Reportar não conformidades é:",
             "opcoes": ["Opcional", "Obrigatório e ético", "Ignorado"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é opcional.",
                 "Correto: Reportar ajuda a prevenir acidentes e falhas.",
                 "Errado: Não deve ser ignorado."]
            },
            {"pergunta": "Ergonomia adequada evita:",
             "opcoes": ["Acidentes e doenças ocupacionais", "Nada", "Redução de produção"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Evita lesões e doenças.",
                 "Errado: Não é irrelevante.",
                 "Errado: Não reduz produção se aplicado corretamente."]
            },
            {"pergunta": "Checklists ajudam a:",
             "opcoes": ["Padronizar processos e reduzir erros", "Aumentar riscos", "Ignorar normas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Checklists melhoram segurança e qualidade.",
                 "Errado: Não aumentam riscos.",
                 "Errado: Não ignoram normas."]
            },
            {"pergunta": "Participar das CIPA meetings é:",
             "opcoes": ["Obrigatório e ético", "Opcional", "Somente para supervisores"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Reforça cultura de segurança.",
                 "Errado: Não é opcional.",
                 "Errado: Não só supervisores."]
            },
            {"pergunta": "Uso correto de ferramentas significa:",
             "opcoes": ["Segurança e eficiência", "Risco aumentado", "Irrelevante"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Garante segurança e ética.",
                 "Errado: Não aumenta risco.",
                 "Errado: Não é irrelevante."]
            },
            {"pergunta": "Seguir normas internas é:",
             "opcoes": ["Obrigatório e ético", "Opcional", "Depende do supervisor"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Seguir normas é obrigatório.",
                 "Errado: Não é opcional.",
                 "Errado: Não depende do supervisor."]
            },
            {"pergunta": "Treinamentos periódicos contribuem para:",
             "opcoes": ["Segurança e cultura ética", "Nada", "Somente produtividade"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Treinamentos fortalecem ética e segurança.",
                 "Errado: Não é irrelevante.",
                 "Errado: Não só produtividade."]
            },
            {"pergunta": "Comunicação clara ajuda a:",
             "opcoes": ["Evitar acidentes e conflitos", "Criar problemas", "Ignorar normas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Comunicação clara reduz riscos e erros.",
                 "Errado: Não cria problemas.",
                 "Errado: Não ignora normas."]
            }
        ]
    }
    # Você pode adicionar Compliance, Assédio, Normas Regulamentadoras seguindo o mesmo modelo
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
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}

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
        else:
            st.error("Informe seu e-mail.")

# ---------- TELA DE TÓPICOS ----------
def show_topic(topic_name):
    st.header(topic_name)
    st.write(TOPICOS[topic_name]["conteudo"])
    for i, q in enumerate(TOPICOS[topic_name]["questoes"]):
        st.write(f"**{i+1}. {q['pergunta']}**")
        choice = st.radio(f"Escolha:", q["opcoes"], key=f"{topic_name}_{i}")
        if st.button("Responder", key=f"btn_{topic_name}_{i}"):
            correta_idx = q["resposta"]
            if q["opcoes"].index(choice) == correta_idx:
                st.success("Resposta correta!")
            else:
                st.error("Resposta incorreta!")
            st.info("Explicações:")
            for e in q["explicacao"]:
                st.write(e)
            # Salvar resposta
            save_user_data(st.session_state["user"]["email"], {
                "
