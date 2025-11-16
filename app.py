# app.py
import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


# ---------------- CONFIG ----------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
ADMIN_EMAIL = "kevin.172062@fmm.org.br"

st.set_page_config(page_title="Simulador Ético Industrial", layout="wide")

# ---------------- TOPICOS (conteúdo + 10 questões cada) ----------------
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

    "Boas Práticas": {
        "conteudo": (
            "Boas práticas industriais incluem organização, limpeza, padronização e comunicação eficiente. "
            "Seguir 5S, realizar checklists, reportar não conformidades, manter áreas limpas e organizar materiais garantem segurança e eficiência."
        ),
        "questoes": [
            {"pergunta": "Qual o objetivo do 5S Seiri (Senso de Utilização)?",
             "opcoes": ["Separar o que é necessário do que não é", "Padronizar operações", "Treinar a equipe"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Seiri é separar o útil do inútil.",
                 "Errado: Padronização é Seiketsu/Seiton.",
                 "Errado: Treinamento é consequência, não definição do Seiri."]
            },
            {"pergunta": "O que significa Poka-Yoke?",
             "opcoes": ["Dispositivos à prova de erro", "Aumento de produção", "Gestão visual"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Poka-Yoke previne erros humanos.",
                 "Errado: Não é foco de produtividade em si.",
                 "Errado: Gestão visual é outra prática do Lean."]
            },
            {"pergunta": "Um operador que ignora uma não conformidade para manter a produção está:",
             "opcoes": ["Agindo corretamente para metas", "Colocando em risco a segurança e qualidade", "Resolvendo problema depois"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é correto priorizar metas sobre segurança.",
                 "Correto: Ignorar não conformidade gera risco.",
                 "Errado: Resolver depois pode ser tarde demais."]
            },
            {"pergunta": "Qual a relação entre 5S e segurança?",
             "opcoes": ["Nenhuma", "Melhora organização e reduz riscos", "Apenas estética"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Existe relação direta.",
                 "Correto: Organização reduz acidentes e facilita respostas.",
                 "Errado: Não é só estética."]
            },
            {"pergunta": "Qual ferramenta ajuda a reduzir tempo de setup?",
             "opcoes": ["SMED", "Andon", "CIP"], 
             "resposta": 0,
             "explicacao": [
                 "Correto: SMED é para redução de setup.",
                 "Errado: Andon sinaliza problemas em linha.",
                 "Errado: CIP não é ferramenta comum nesse contexto."]
            },
            {"pergunta": "O que é Jidoka?",
             "opcoes": ["Parar a produção diante de anomalia", "Aumentar velocidade da linha", "Relatório mensal"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Jidoka para a linha quando há problema.",
                 "Errado: Não visa velocidade.",
                 "Errado: Não é relatório."]
            },
            {"pergunta": "Trabalhar segundo POP significa:",
             "opcoes": ["Seguir Procedimento Operacional Padrão", "Criar improvisos", "Ignorar normas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: POP é padronização da tarefa.",
                 "Errado: Improvisos são risco.",
                 "Errado: POP visa cumprir normas."]
            },
            {"pergunta": "O que é gestão visual?",
             "opcoes": ["Uso de sinais e indicadores para facilitar decisões", "Somente decoração", "Somente controle de estoque"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Gestão visual facilita comunicação imediata.",
                 "Errado: Não é decoração.",
                 "Errado: Vai além de estoque."]
            },
            {"pergunta": "Como o Kaizen contribui com boas práticas?",
             "opcoes": ["Melhoria contínua com pequenas mudanças", "Troca constante de processos", "Eliminação total da fiscalização"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Kaizen melhora constantemente por pequenos ajustes.",
                 "Errado: Não é troca constante sem análise.",
                 "Errado: Fiscalização ainda é necessária."]
            },
            {"pergunta": "Por que registrar não conformidades é importante?",
             "opcoes": ["Rastreabilidade e aprendizado", "Para punir colegas", "Apenas burocracia"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Registro permite ação corretiva e preventiva.",
                 "Errado: Não é para punição apenas.",
                 "Errado: Não é apenas burocracia."]
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

    "Assédio moral e sexual": {
        "conteudo": (
            "Assédio moral envolve humilhação, intimidação ou tratamento desigual repetido. "
            "Assédio sexual inclui comentários, gestos ou convites indesejados de cunho sexual. "
            "É obrigação ética e legal reportar imediatamente qualquer situação de assédio."
        ),
        "questoes": [
            {"pergunta": "O que caracteriza assédio moral?",
             "opcoes": ["Intimidação e humilhação", "Treinamento diário", "Reuniões de equipe"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Assédio moral envolve intimidação e humilhação.",
                 "Errado: Treinamento não é assédio.",
                 "Errado: Reuniões não configuram assédio."]
            },
            {"pergunta": "Assédio sexual é:",
             "opcoes": ["Comentários ou gestos indesejados", "Feedback de desempenho", "Planejamento de produção"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Assédio sexual envolve comportamento indesejado.",
                 "Errado: Feedback não é assédio.",
                 "Errado: Planejamento não é assédio."]
            },
            {"pergunta": "Se você testemunhar assédio, deve:",
             "opcoes": ["Reportar imediatamente", "Ignorar", "Participar"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Reportar é obrigação ética.",
                 "Errado: Ignorar é antiético.",
                 "Errado: Participar é errado."]
            },
            {"pergunta": "Assédio repetitivo, mesmo sutil, é:",
             "opcoes": ["Inaceitável", "Aceitável", "Normal"],
             "resposta": 0,
             "explicacao": [
                 "Correto: É inaceitável.",
                 "Errado: Não é aceitável.",
                 "Errado: Não é normal."]
            },
            {"pergunta": "Comentários sobre aparência de colegas é:",
             "opcoes": ["Pode ser assédio", "Sempre permitido", "Ignorado"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Pode configurar assédio sexual.",
                 "Errado: Nem sempre permitido.",
                 "Errado: Não deve ser ignorado."]
            },
            {"pergunta": "Exigir favores pessoais é:",
             "opcoes": ["Assédio", "Treinamento", "Parte da função"],
             "resposta": 0,
             "explicacao": [
                 "Correto: É assédio.",
                 "Errado: Não é treinamento.",
                 "Errado: Não faz parte da função."]
            },
            {"pergunta": "Comentários discriminatórios são:",
             "opcoes": ["Assédio moral", "Apropriados", "Normais"],
             "resposta": 0,
             "explicacao": [
                 "Correto: São assédio moral.",
                 "Errado: Não são apropriados.",
                 "Errado: Não são normais."]
            },
            {"pergunta": "Intimidação no trabalho é:",
             "opcoes": ["Assédio moral", "Treinamento", "Reunião normal"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Configura assédio moral.",
                 "Errado: Não é treinamento.",
                 "Errado: Não é reunião normal."]
            },
            {"pergunta": "Se um colega recusa avanços indesejados, você deve:",
             "opcoes": ["Respeitar a decisão", "Insistir", "Ignorar normas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Sempre respeitar.",
                 "Errado: Não insistir.",
                 "Errado: Não ignorar normas éticas."]
            },
            {"pergunta": "Denunciar assédio protege:",
             "opcoes": ["Vítima e ética no trabalho", "Somente testemunha", "Não ajuda ninguém"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Protege a vítima e reforça ética.",
                 "Errado: Não é só testemunha.",
                 "Errado: Ajuda sim todos na empresa."]
            }
        ]
    },

    "Normas Regulamentadoras": {
        "conteudo": (
            "As Normas Regulamentadoras (NRs) definem obrigações legais e práticas de segurança e saúde no trabalho. "
            "Exemplos: NR-6 (EPI), NR-12 (segurança em máquinas e equipamentos), NR-26 (sinalização de segurança), NR-17 (ergonomia). "
            "O cumprimento das NRs garante ética, proteção da integridade física e legalidade das operações."
        ),
        "questoes": [
            {"pergunta": "Qual NR trata do uso obrigatório de EPIs?",
             "opcoes": ["NR-6", "NR-12", "NR-26"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-6 define obrigatoriedade de Equipamentos de Proteção Individual.",
                 "Errado: NR-12 trata de segurança de máquinas.",
                 "Errado: NR-26 trata de sinalização."]
            },
            {"pergunta": "A NR-12 é voltada para:",
             "opcoes": ["Segurança de máquinas e equipamentos", "Sinalização de risco", "Organização do ambiente"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-12 estabelece requisitos para máquinas.",
                 "Errado: NR-26 trata de sinalização.",
                 "Errado: Organização do ambiente não é foco principal."]
            },
            {"pergunta": "A NR-26 trata de:",
             "opcoes": ["Sinalização de segurança", "EPI", "Treinamento de operadores"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-26 estabelece cores, símbolos e sinais de segurança.",
                 "Errado: EPI é NR-6.",
                 "Errado: Treinamento não é foco da NR-26."]
            },
            {"pergunta": "Cumprir as NRs é:",
             "opcoes": ["Obrigatório e ético", "Opcional", "Somente para gerência"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Cumprir NRs é exigência legal e ética.",
                 "Errado: Não é opcional.",
                 "Errado: Aplica-se a todos, não só gerência."]
            },
            {"pergunta": "A NR-17 trata de:",
             "opcoes": ["Ergonomia no trabalho", "Uso de EPIs", "Sinalização de risco"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-17 define ergonomia e condições adequadas para operadores.",
                 "Errado: EPIs são NR-6.",
                 "Errado: Sinalização é NR-26."]
            },
            {"pergunta": "Ignorar as NRs pode resultar em:",
             "opcoes": ["Acidentes e penalidades legais", "Aumento de produção", "Reconhecimento ético"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Ignorar NRs coloca vidas em risco e gera punições.",
                 "Errado: Não necessariamente aumenta produção.",
                 "Errado: Não gera reconhecimento ético."]
            },
            {"pergunta": "Dispositivos de bloqueio (lockout/tagout) são exigidos por qual NR?",
             "opcoes": ["NR-12", "NR-6", "NR-17"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-12 exige bloqueio de máquinas para manutenção segura.",
                 "Errado: NR-6 é sobre EPIs.",
                 "Errado: NR-17 é ergonomia."]
            },
            {"pergunta": "Sinalização de segurança deve ser clara para:",
             "opcoes": ["Todos os colaboradores", "Apenas supervisores", "Apenas visitantes"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Todos precisam reconhecer riscos.",
                 "Errado: Não só supervisores.",
                 "Errado: Não só visitantes."]
            },
            {"pergunta": "Treinamentos sobre NRs devem ser:",
             "opcoes": ["Periódicos e obrigatórios", "Esporádicos", "Opcional"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Treinamentos periódicos garantem segurança e ética.",
                 "Errado: Não apenas esporádicos.",
                 "Errado: Não é opcional."]
            },
            {"pergunta": "O cumprimento das NRs reflete na ética porque:",
             "opcoes": ["Protege operadores e respeita a lei", "Só aumenta burocracia", "Não tem impacto"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Seguir NRs é agir eticamente e proteger a vida.",
                 "Errado: Não é apenas burocracia.",
                 "Errado: Tem impacto direto."]
            }
        ]
    }
}

# ---------------- FUNÇÕES DE DADOS ----------------
def save_user_data_raw(user_email, payload):
    """
    payload: dict (will be appended to user's history list)
    """
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    existing = {"history": []}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            existing = {"history": []}
    existing.setdefault("history", []).append(payload)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')

def load_user_data(user_email):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    if not path.exists():
        return {"history": []}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {"history": []}

# ---------------- HELPERS ----------------
def initialize_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "modo_questoes" not in st.session_state:
        st.session_state["modo_questoes"] = False
    if "topico_atual" not in st.session_state:
        st.session_state["topico_atual"] = None
    if "questao_atual" not in st.session_state:
        st.session_state["questao_atual"] = 0
    if "acertos" not in st.session_state:
        st.session_state["acertos"] = 0

# ---------------- UI - LOGIN ----------------
def login_screen():
    st.header("Simulador Ético Industrial — Acesso")
    if st.session_state["user"] is None:
        col1, col2 = st.columns([3,2])
        with col1:
            name = st.text_input("Nome", key="login_name")
            email = st.text_input("Email (use seu e-mail institucional)", key="login_email")
        with col2:
            st.write("")
            st.write("")
            if st.button("Entrar"):
                if email:
                    st.session_state["user"] = {"name": name.strip() or "Usuário", "email": email.strip()}
                    st.success(f"Olá, {st.session_state['user']['name']}! Você está logado.")
                else:
                    st.error("Informe seu e-mail para continuar.")
        return False
    else:
        st.sidebar.markdown(f"**Logado como:** {st.session_state['user']['name']}  \n{st.session_state['user']['email']}")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.clear()
            initialize_session()
            st.experimental_rerun()
        return True

# ---------------- Mostrar aula (conteúdo) ----------------
def mostrar_aula(topico):
    st.subheader(f"Aula — {topico}")
    st.info(TOPICOS[topico]["conteudo"])

# ---------------- TELA DE TÓPICOS E QUESTÕES ----------------
def topico_screen():
    st.title("Tópicos de Treinamento")
    col1, col2 = st.columns([3,1])
    with col1:
        topico_escolhido = st.selectbox("Escolha o tópico", list(TOPICOS.keys()))
        mostrar_aula(topico_escolhido)
    with col2:
        st.markdown("**Controles**")
        if st.button("📚 Iniciar caderno de questões"):
            st.session_state["modo_questoes"] = True
            st.session_state["topico_atual"] = topico_escolhido
            st.session_state["questao_atual"] = 0
            st.session_state["acertos"] = 0

    # modo questões (uma por vez)
    if st.session_state["modo_questoes"]:
        topico = st.session_state["topico_atual"]
        questoes = TOPICOS[topico]["questoes"]
        idx = st.session_state["questao_atual"]
        if idx < 0:
            idx = 0
            st.session_state["questao_atual"] = 0

        st.markdown("---")
        st.subheader(f"Questão {idx+1} / {len(questoes)} — {topico}")
        q = questoes[idx]
        st.write(f"**{q['pergunta']}**")
        escolha = st.radio("Escolha uma opção:", q["opcoes"], key=f"radio_{topico}_{idx}")

        cola, colb, colc = st.columns([1,1,1])
        with cola:
            if st.button("Confirmar resposta", key=f"confirm_{topico}_{idx}"):
                acertou = (q["opcoes"].index(escolha) == q["resposta"])
                if acertou:
                    st.success("✔ Resposta correta!")
                    st.session_state["acertos"] += 1
                else:
                    st.error("❌ Resposta incorreta.")
                # mostra explicação detalhada para a opção escolhida e a correta
                explained_index = q["opcoes"].index(escolha)
                st.info(f"💡 Explicação para sua escolha: {q['explicacao'][explained_index]}")
                # Também pode mostrar a resposta correta
                st.write(f"**Resposta correta:** {q['opcoes'][q['resposta']]}")
                st.write("")

                # salvar resultado parcial no histórico
                payload = {
                    "timestamp": datetime.now().isoformat(),
                    "topico": topico,
                    "pergunta": q["pergunta"],
                    "resposta_escolhida": escolha,
                    "resposta_correta": q["opcoes"][q["resposta"]],
                    "acertou": bool(acertou)
                }
                save_user_data_raw(st.session_state["user"]["email"], payload)

        with colb:
            if st.button("➡ Próxima questão", key=f"next_{topico}_{idx}"):
                if idx + 1 < len(questoes):
                    st.session_state["questao_atual"] += 1
                else:
                    # finalizou
                    st.session_state["modo_questoes"] = False
                    st.success("🎉 Você finalizou o caderno de questões!")
        with colc:
            if st.button("🔁 Encerrar e ver resultado", key=f"finish_{topico}_{idx}"):
                st.session_state["modo_questoes"] = False

        # se finalizou (quando idx == last and user pressed confirm), mostrar resumo
        if (idx + 1) > len(questoes) - 1 and not st.session_state["modo_questoes"]:
            # mostrar resultado geral do attempt (conteúdo salvo já em JSON)
            st.write("---")
            st.write(f"Resultado acumulado nesta sessão: **{st.session_state['acertos']} / {len(questoes)}**")
            cb = st.text_area("Deixe um feedback sobre o tópico (opcional):", key=f"fb_final_{topico}")
            if st.button("Salvar feedback final"):
                payload = {
                    "timestamp": datetime.now().isoformat(),
                    "topico": topico,
                    "pergunta": "Feedback final",
                    "resposta_escolhida": None,
                    "resposta_correta": None,
                    "acertou": None,
                    "feedback": cb
                }
                save_user_data_raw(st.session_state["user"]["email"], payload)
                st.success("Feedback salvo!")

# ---------------- TELA DE PERFORMANCE (GRÁFICOS) ----------------
def performance_screen():
    st.title("Desempenho do Usuário")
    user = st.session_state["user"]
    if user is None:
        st.info("Por favor, faça login para ver seu desempenho.")
        return

    data = load_user_data(user["email"])
    history = data.get("history", [])
    if not history:
        st.info("Nenhuma resposta registrada ainda.")
        return

    df = pd.DataFrame(history)

    # Agregar por tópico: contar acertos vs erros
    grouped = df.groupby(["topico", "acertou"]).size().unstack(fill_value=0)
    # garantir colunas True/False existam
    if True not in grouped.columns:
        grouped[True] = 0
    if False not in grouped.columns:
        grouped[False] = 0

    st.write("Resumo por tópico:")
    for topico in grouped.index:
        acertos = int(grouped.loc[topico][True]) if True in grouped.columns else 0
        erros = int(grouped.loc[topico][False]) if False in grouped.columns else 0
        total = acertos + erros
        if total == 0:
            continue
        fig = px.pie(names=["Acertos", "Erros"], values=[acertos, erros],
                     title=f"{topico} — {acertos}/{total} acertos", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    # Também mostrar tabela cronológica
    st.write("---")
    st.subheader("Histórico (cronológico)")
    df_show = df.copy()
    # mostrar colunas relevantes
    cols = ["timestamp", "topico", "pergunta", "resposta_escolhida", "resposta_correta", "acertou"]
    for c in cols:
        if c not in df_show.columns:
            df_show[c] = None
    st.dataframe(df_show[cols].sort_values("timestamp", ascending=False).reset_index(drop=True))

# ---------------- TELA ADMIN ----------------
def admin_screen():
    st.title("Administração (Apenas admin)")
    user = st.session_state["user"]
    if user is None or user.get("email") != ADMIN_EMAIL:
        st.error("Acesso restrito ao administrador.")
        return
    all_files = list(DATA_DIR.glob("*.json"))
    if not all_files:
        st.info("Nenhum dado encontrado.")
        return

    combined = []
    for f in all_files:
        email = f.stem.replace("_at_", "@")
        data = load_user_data(email)
        for h in data.get("history", []):
            row = h.copy()
            row["email"] = email
            combined.append(row)

    if not combined:
        st.info("Nenhum histórico encontrado.")
        return

    df = pd.DataFrame(combined)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Exportar CSV com todos os resultados", data=csv, file_name="resultados_simulador.csv", mime="text/csv")

# ---------------- MAIN ----------------
def main():
    initialize_session()
    logged = login_screen()
    if not logged:
        return

    # menu lateral
    st.sidebar.title("Menu")
    tela = st.sidebar.selectbox("Escolha a tela", ["Tópicos", "Desempenho", "Administração"])
    st.sidebar.markdown("---")
    st.sidebar.write("Versão: 1.0")
    st.sidebar.write("Usuário: " + (st.session_state["user"]["email"] if st.session_state["user"] else "—"))

    if tela == "Tópicos":
        topico_screen()
    elif tela == "Desempenho":
        performance_screen()
    elif tela == "Administração":
        admin_screen()

if __name__ == "__main__":
    main()
