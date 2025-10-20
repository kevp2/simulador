# app.py
import streamlit as st
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import csv

# ---------- CONFIG ----------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

ADMIN_EMAIL = "kevin.172062@fmm.org.br"

# ---------- TOPICOS (conteúdo técnico interpretado + questões com explicações) ----------
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
             "opcoes": ["Consertar sozinho e usar normalmente",
                        "Comunicar e aguardar substituição",
                        "Continuar sem EPI se for rápido"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Consertar sozinho pode colocar sua vida em risco.",
                 "Correto: Comunicar imediatamente e aguardar substituição é o procedimento correto e ético.",
                 "Errado: Continuar sem EPI é uma violação das normas de segurança e ética."]
            },
            {"pergunta": "Antes de realizar manutenção em uma máquina (NR-12), qual procedimento é obrigatório?",
             "opcoes": ["Desligar e começar a mexer",
                        "Aplicar lockout/tagout e verificar ausência de energia",
                        "Pedir permissão verbal e continuar"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Apenas desligar não garante segurança.",
                 "Correto: Lockout/tagout garante que não haverá energia acidental, prevenindo acidentes.",
                 "Errado: Permissão verbal não substitui bloqueio físico."]
            },
            {"pergunta": "Ao detectar fumaça leve num painel elétrico, a atitude correta é:",
             "opcoes": ["Continuar a produção",
                        "Isolar a área e acionar manutenção/leadership",
                        "Esperar até o fim do turno"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Ignorar risco pode gerar acidente grave.",
                 "Correto: Isolar e acionar manutenção garante segurança imediata.",
                 "Errado: Esperar não previne o risco."]
            },
            {"pergunta": "Relatar quase-acidentes é importante porque:",
             "opcoes": ["Serve apenas para estatística",
                        "Previne acidentes futuros ao permitir ações corretivas",
                        "É irrelevante se ninguém se feriu"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não serve apenas para estatística, tem função preventiva.",
                 "Correto: Permite melhorar processos e prevenir acidentes.",
                 "Errado: Ignorar near-misses reduz segurança."]
            },
            {"pergunta": "Qual tem prioridade na hierarquia de controles de risco?",
             "opcoes": ["EPIs",
                        "Medidas coletivas (eliminar/mitigar risco)",
                        "Procedimentos informais"],
             "resposta": 1,
             "explicacao": [
                 "Errado: EPIs são importantes mas complementares.",
                 "Correto: Medidas coletivas (proteções físicas, barreiras) têm prioridade.",
                 "Errado: Procedimentos informais não garantem segurança."]
            },
            {"pergunta": "Se uma proteção de máquina estiver danificada durante troca de ferramenta, você:",
             "opcoes": ["Continua e avisa depois",
                        "Interrompe e não opera até corrigir",
                        "Tapa a proteção com fita"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Continuar expõe a todos a risco.",
                 "Correto: Interromper garante segurança até reparo.",
                 "Errado: Improvisações não são seguras."]
            },
            {"pergunta": "O papel ético do operador quanto ao EPI é:",
             "opcoes": ["Usar e zelar pelo EPI; reportar problemas",
                        "Evitar uso para maior conforto",
                        "Compartilhar com colegas sem checar"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Usar corretamente protege a si e aos colegas.",
                 "Errado: Evitar uso compromete segurança.",
                 "Errado: Compartilhar sem verificação não é seguro."]
            },
            {"pergunta": "Para controlar exposição a agentes químicos do PGR/PPRA, o melhor é:",
             "opcoes": ["Ignorar fichas técnicas",
                        "Aplicar controles coletivos, ventilação e EPIs quando necessário",
                        "Acelerar tarefas sem proteção"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Ignorar fichas é arriscado.",
                 "Correto: Seguir controles coletivos e EPIs garante proteção.",
                 "Errado: Acelerar sem proteção aumenta riscos."]
            },
        ],
    },

    # ------ Demais tópicos resumidos para espaço ------

    "Compliance": {
        "conteudo": "Compliance refere-se a práticas e controles que asseguram o cumprimento de leis, normas internas e ética industrial.",
        "questoes": [
            {"pergunta": "Se um operador souber de conduta antiética, ele deve:",
             "opcoes": ["Ignorar", "Reportar pelos canais formais", "Divulgar em redes sociais"],
             "resposta": 1,
             "explicacao": ["Errado: Ignorar permite irregularidades.", "Correto: Reportar formalmente é o adequado.", "Errado: Redes sociais não são canais oficiais."]}
        ],
    },

    "Boas práticas no trabalho": {
        "conteudo": "Boas práticas incluem 5S, passagem de turno estruturada, uso correto de ferramentas e comunicação assertiva.",
        "questoes": [
            {"pergunta": "O 5S visa:",
             "opcoes": ["Organização, limpeza e padronização", "Aumentar risco", "Substituir manutenção"],
             "resposta": 0,
             "explicacao": ["Correto: 5S organiza e padroniza.", "Errado: 5S não aumenta risco.", "Errado: 5S não substitui manutenção."]}
        ],
    },

    "Assédio moral e sexual": {
        "conteudo": "Condutas que atentam contra a dignidade do trabalhador. A empresa deve oferecer canais de denúncia e proteção à vítima.",
        "questoes": [
            {"pergunta": "Se presenciar assédio sexual, o correto é:",
             "opcoes": ["Ignorar", "Notificar e apoiar a vítima; usar canais formais", "Divulgar nas redes sociais"],
             "resposta": 1,
             "explicacao": ["Errado: Ignorar perpetua o problema.", "Correto: Reportar formalmente protege a vítima.", "Errado: Redes sociais não são canais seguros."]}
        ],
    },

    "Normas Regulamentadoras": {
        "conteudo": "NRs definem requisitos mínimos de SST. Aplicá-las significa traduzir regras em procedimentos operacionais.",
        "questoes": [
            {"pergunta": "A NR-6 trata de:",
             "opcoes": ["EPIs", "Máquinas", "Ergonomia"],
             "resposta": 0,
             "explicacao": ["Correto: NR-6 é sobre EPIs.", "Errado: NR-6 não trata de máquinas.", "Errado: NR-6 não trata de ergonomia."]}
        ],
    },
}

# ---------- HELPERS ----------
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

# ---------- AUTH SIMULADO ----------
def login_screen():
    st.header("Simulador Ético Industrial — Acesso")
    st.write("Faça login para iniciar o treinamento.")
    name = st.text_input("Nome", key="mock_name")
    email = st.text_input("Email", key="mock_email")
    if st.button("Entrar"):
        if email:
            st.session_state["user"] = {"name": name, "email": email}
            st.success(f"Olá, {name}! Login efetuado.")
            st.experimental_rerun()
        else:
            st.error("Informe seu e-mail para continuar.")

# ---------- TELA PRINCIPAL ----------
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
        for idx, q in enumerate(topic_data["questoes"]):
            correta = q["opcoes"][q["resposta"]]
            escolhida = respostas[idx]
            acertou = escolhida == correta
            if acertou:
                score += 1
            # Exibir explicação
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
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        save_user_data(user_email, payload)

# ---------- TELA DE DADOS ----------
def show_user_data(user_email):
    st.header("Dados do seu desempenho")
    data = get_aggregate_for_user(user_email)
    if not data or "history" not in data:
        st.info("Nenhum dado disponível.")
        return
    df = pd.DataFrame(data["history"])
    for topic in df["topic"].unique():
        st.subheader(topic)
        topic_scores = df[df["topic"] == topic]["score"]
        st.line_chart(topic_scores)
    st.dataframe(df[["topic", "score", "feedback", "timestamp"]])

# ---------- TELA ADMINISTRAÇÃO ----------
def show_admin():
    st.header("Administração — Exportar CSV")
    csv_path = DATA_DIR / "consolidado.csv"
    
    all_data = []
    for file in DATA_DIR.glob("*.json"):
        user_data = json.loads(file.read_text(encoding="utf-8"))
        email = file.stem.replace("_at_", "@")
        for entry in user_data.get("history", []):
            all_data.append({
                "email": email,
                "topic": entry.get("topic"),
                "score": entry.get("score"),
                "feedback": entry.get("feedback"),
                "timestamp": entry.get("timestamp")
            })
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        st.success(f"CSV consolidado criado em {csv_path}")
        st.download_button("Baixar CSV consolidado", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="consolidado.csv")

# ---------- MAIN ----------
def main():
    st.set_page_config(page_title="Simulador Ético Industrial", layout="wide")
    initialize_session()
    
    if "user" not in st.session_state:
        login_screen()
        return
    
    user = st.session_state["user"]
    st.sidebar.title(f"Bem-vindo, {user['name']}!")
    
    # Menu
    menu_options = ["Tópicos", "Dados"]
    if user["email"].lower() == ADMIN_EMAIL:
        menu_options.append("Administração")
    
    choice = st.sidebar.radio("Navegação", menu_options)
    
    if choice == "Tópicos":
        st.header("Selecione o tópico")
        topic_name = st.selectbox("Tópico", list(TOPICOS.keys()))
        show_topic(topic_name, TOPICOS[topic_name], user["email"])
    elif choice == "Dados":
        show_user_data(user["email"])
    elif choice == "Administração":
        show_admin()

if __name__ == "__main__":
    main()
