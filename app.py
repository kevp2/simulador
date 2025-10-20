## app.py
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

# ---------- TOPICOS ----------
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
            # ... total de 10 questões no mesmo formato ...
        ],
    },
    "Compliance": {
        "conteudo": (
            "Compliance industrial garante que todos os colaboradores atuem dentro das normas legais, regulamentares e éticas. "
            "Inclui políticas internas, código de conduta, canais de denúncia e prevenção de fraudes. "
            "A NR-1 (Disposições Gerais) estabelece a obrigatoriedade de cumprimento de normas regulamentadoras e a NR-5 (CIPA) reforça a participação de colaboradores na gestão de riscos. "
            "Exemplo aplicado: se um operador identifica que um procedimento de manutenção está sendo ignorado, o correto é reportar pelo canal formal, mesmo que a produção esteja pressionada. "
            "Isso demonstra integridade ética e protege colegas. Diferenciação: Compliance não é apenas seguir regras, mas promover cultura ética, prevenir desvios e garantir rastreabilidade das ações."
        ),
        "questoes": [
            {"pergunta": "Se um operador identificar um procedimento ignorado que possa causar acidente, ele deve:",
             "opcoes": ["Ignorar", "Reportar formalmente", "Contornar sem avisar"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Ignorar permite irregularidades.",
                 "Correto: Reportar formalmente é o procedimento ético e seguro.",
                 "Errado: Contornar sem avisar coloca todos em risco."]
            },
            # ... total de 10 questões ...
        ],
    },
    "Boas práticas no trabalho": {
        "conteudo": (
            "Boas práticas incluem: 5S, passagem de turno estruturada, uso correto de ferramentas, comunicação clara e ergonomia. "
            "Exemplo aplicado: manter ferramentas em local organizado, anotar observações na passagem de turno, seguir checklist de operação, usar EPI corretamente. "
            "Riscos de não aplicar: retrabalho, acidentes, desperdício de recursos, falhas em auditorias."
        ),
        "questoes": [
            {"pergunta": "O 5S visa:",
             "opcoes": ["Organização, limpeza e padronização", "Substituir manutenção", "Aumentar risco"],
             "resposta": 0,
             "explicacao": [
                 "Correto: 5S organiza, padroniza e mantém segurança.",
                 "Errado: Não substitui manutenção.",
                 "Errado: Não aumenta risco, pelo contrário reduz."]
            },
            # ... total de 10 questões ...
        ],
    },
    "Assédio moral e sexual": {
        "conteudo": (
            "O assédio moral envolve atitudes que humilham, intimidam ou prejudicam o trabalhador repetidamente. "
            "O assédio sexual envolve avanços ou comentários indesejados com conotação sexual. "
            "A NR-1 reforça que a empresa deve adotar medidas preventivas e canais seguros de denúncia. "
            "A ética industrial exige respeito à dignidade do trabalhador. Exemplo: Se um operador presencia ou sofre assédio, deve usar canais de denúncia formais."
        ),
        "questoes": [
            {"pergunta": "Assédio moral é:",
             "opcoes": ["Repetidas humilhações", "Uma crítica construtiva", "Comunicação clara"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Assédio moral é humilhação repetida.",
                 "Errado: Crítica construtiva não é assédio.",
                 "Errado: Comunicação clara não é assédio."]
            },
            # ... total de 10 questões ...
        ],
    },
    "Normas Regulamentadoras": {
        "conteudo": (
            "As NRs estabelecem requisitos mínimos de segurança e saúde no trabalho. "
            "Exemplos: NR-6 (EPI), NR-12 (máquinas), NR-17 (ergonomia), NR-26 (sinalização), NR-35 (trabalho em altura). "
            "Aplicação correta significa traduzir regras em práticas operacionais seguras e éticas."
        ),
        "questoes": [
            {"pergunta": "NR-6 trata de:",
             "opcoes": ["EPIs", "Máquinas", "Ergonomia"],
             "resposta": 0,
             "explicacao": [
                 "Correto: NR-6 trata de EPIs.",
                 "Errado: NR-6 não trata de máquinas.",
                 "Errado: NR-6 não trata de ergonomia."]
            },
            # ... total de 10 questões ...
        ],
    },
}

# ---------- FUNÇÕES DE SALVAMENTO E CARREGAMENTO ----------
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

# ---------- LOGIN SIMULADO ----------
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
