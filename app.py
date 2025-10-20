# app.py
import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
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
    "Boas práticas": {
        "conteudo": (
            "Boas práticas industriais incluem organização, limpeza, padronização e comunicação eficiente. "
            "Seguir 5S, realizar checklists, reportar não conformidades, manter áreas limpas e organizar materiais garantem segurança e eficiência."
        ),
        "questoes": [
            # Aqui inserir o bloco de 10 questões completas de Boas Práticas que te enviei anteriormente
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
    "Compliance": {
        "conteudo": (
            "Compliance industrial garante que todos os colaboradores atuem dentro das normas legais, regulamentares e éticas. "
            "Inclui políticas internas, código de conduta, canais de denúncia, prevenção de fraudes e cumprimento das NRs."
        ),
        "questoes": [
            # Inserir bloco completo de 10 questões de Compliance
            
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
            # Inserir bloco completo de 10 questões de Assédio Moral e Sexual
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
            # Inserir bloco completo de 10 questões de Normas Regulamentadoras
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
    },
}

# ---------- FUNÇÕES ----------
def save_user_data(user_email, payload):
    path = DATA_DIR / f"{user_email.replace('@','_at_')}.json"
    existing = {}
    if path.exists():
        existing = json.loads(path.read_text(encoding='utf-8'))
    existing.setdefault("history", []).append(payload)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')

def get_aggregate_for_user(user_email):
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
    st.header("Simulador Ético Industrial — Acesso")
    st.write("Faça login para iniciar o treinamento.")
    name = st.text_input("Nome")
    email = st.text_input("Email")
    if st.button("Entrar"):
        if email:
            st.session_state["user"] = {"name": name, "email": email}
            st.success(f"Olá, {name}! Login efetuado.")
            st.experimental_rerun()
        else:
            st.error("Informe seu e-mail para continuar.")
    # Botão logout aparece se já houver sessão
    if st.session_state.get("user"):
        if st.button("Sair"):
            st.session_state.pop("user")
            st.success("Logout realizado.")
            st.experimental_rerun()

# ---------- TELA DE TÓ
