# app.py
import streamlit as st
import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------- CONFIG ----------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
ADMIN_EMAIL = "kevin.172062@fmm.org.br"

# ---------- TOPICOS COMPLETOS COM 10 QUESTÕES ----------
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
            {"pergunta": "Qual a finalidade da NR-12?",
             "opcoes": ["Regular uso de EPIs", "Garantir segurança na operação de máquinas", "Definir jornadas de trabalho"],
             "resposta": 1,
             "explicacao": [
                 "Errado: NR-6 regula EPIs.",
                 "Correto: NR-12 garante segurança na operação de máquinas.",
                 "Errado: NR-12 não define jornadas."]
            },
            {"pergunta": "O que é lockout/tagout?",
             "opcoes": ["Procedimento de parada segura de máquinas", "Treinamento de liderança", "Plano de férias do operador"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Lockout/tagout é parada segura de máquinas.",
                 "Errado: Não é treinamento de liderança.",
                 "Errado: Não tem relação com férias."]
            },
            {"pergunta": "Quando é obrigatório usar EPI?",
             "opcoes": ["Quando houver risco residual", "Somente se o supervisor pedir", "Nunca é obrigatório"],
             "resposta": 0,
             "explicacao": [
                 "Correto: EPI é obrigatório quando houver risco residual.",
                 "Errado: Não depende do supervisor pedir.",
                 "Errado: Sempre há situações obrigatórias."]
            },
            {"pergunta": "Participar de treinamentos de segurança é:",
             "opcoes": ["Opcional", "Obrigatório e ético", "Perda de tempo"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é opcional em termos de ética.",
                 "Correto: Obrigatório e reforça responsabilidade ética.",
                 "Errado: Treinamento não é perda de tempo."]
            },
            {"pergunta": "Reportar um risco identificado é:",
             "opcoes": ["Opcional", "Obrigatório", "Proibido"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é opcional eticamente.",
                 "Correto: É obrigatório reportar riscos.",
                 "Errado: Não é proibido."]
            },
            {"pergunta": "NR-26 trata de:",
             "opcoes": ["Sinalização de segurança", "Proteção de máquinas", "EPIs"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-26 regula sinalização.",
                 "Errado: Não trata de proteção de máquinas.",
                 "Errado: Não trata de EPIs."]
            },
            {"pergunta": "Ergonomia visa:",
             "opcoes": ["Reduzir riscos e melhorar postura", "Aumentar produção sem segurança", "Substituir treinamentos"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Ergonomia reduz riscos e melhora postura.",
                 "Errado: Produção sem segurança é incorreto.",
                 "Errado: Não substitui treinamentos."]
            },
            {"pergunta": "É correto desligar máquinas sem seguir procedimentos?",
             "opcoes": ["Sim", "Não", "Somente se rápido"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é seguro.",
                 "Correto: Sempre siga procedimentos.",
                 "Errado: Velocidade não justifica risco."]
            },
            {"pergunta": "O que um operador deve fazer se perceber falha de segurança?",
             "opcoes": ["Ignorar", "Reportar imediatamente", "Tentar consertar sozinho"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Ignorar é antiético.",
                 "Correto: Reportar imediatamente é a ação ética.",
                 "Errado: Consertar sozinho pode ser perigoso."]
            },
        ]
    },
    # --------- Aqui você acrescenta Compliance, Boas práticas, Assédio e NRs com 10 questões completas ----------
}

# ---------- FUNÇÕES DE SALVAMENTO E DADOS ----------
def save_user_data(user_email, payload):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            existing = {}
    existing.setdefault("history", []).append(payload)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')

def get_aggregate_for_user(user_email):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return data
    except Exception:
        return {}

def initialize_session():
    if "results" not in st.session_state:
        st.session_state["results"] = {}
    if "feedbacks" not in st.session_state:
        st.session_state["feedbacks"] = {}

# ---------- LOGIN ----------
def login_screen():
    st.header("Simulador Ético Industrial — Acesso")
    st.write("Faça login para iniciar o treinamento.")
    name = st.text_input("Nome", key="mock_name")
    email = st.text_input("Email", key="mock_email")
    if st.button("Entrar"):
        if email:
            st.session_state["user"] = {"name": name, "email": email}
            st.success(f"Olá, {name}! Login efetuado.")
            st.stop()  # substitui o experimental_rerun
        else:
            st.error("Informe seu e-mail para continuar.")

# ---------- TELA DE TÓPICOS ----------
def show_topic(topic_name, topic_data, user_email):
    st.subheader(topic_name)
    st.write(topic_data["conteudo"])
    
    respostas = []
    score = 0
    for idx, q in enumerate(topic_data["questoes"]):
        st.markdown(f"**{idx+1}. {q['pergunta']}**")
        opcao = st.radio(f"Escolha uma opção (Pergunta {idx+1})", q["opcoes"], key=f"{topic_name}_{idx}")
        respostas.append(opcao)
    
    if st.button(f"Enviar respostas - {topic_name}"):
        resultados = []
        acertos = 0
        erros = 0
        for idx, q in enumerate(topic_data["questoes"]):
            correta = q["opcoes"][q["resposta"]]
            escolhida = respostas[idx]
            acertou = escolhida == correta
            if acertou:
                score += 1
                acertos += 1
            else:
                erros += 1
            st.markdown(f"**Questão {idx+1}**: Sua resposta: {escolhida}")
            st.write(f"✅ Correta!" if acertou else f"❌ Incorreta!")
            st.write("Explicações:")
            for exp in q["explicacao"]:
                st.write("-", exp)
            resultados.append({"pergunta": q["pergunta"], "resposta_usuario": escolhida, "resposta_correta": correta})
        
        st.success(f"Sua pontuação: {score}/{len(topic_data['questoes'])}")
        feedback = st.text_area("Deixe seu feedback sobre o que aprendeu:")
        payload = {
            "topic": topic_name,
            "score": score,
            "respostas": resultados,
            "feedback": feedba
