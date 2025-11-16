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
def mostrar_conteudo(topico):
    st.title(f"📘 Curso: {topico}")
    
    if topico == "Segurança no Trabalho":
    st.markdown("""
    A Segurança do Trabalho representa a base da ética operacional e é parte essencial da cultura organizacional
    responsável. Sua função vai além da prevenção de acidentes — ela garante a integridade física e psicológica do
    trabalhador, preserva vidas e promove responsabilidade social.

    De acordo com a **NR-1 (Disposições Gerais)**, toda atividade laboral deve garantir condições seguras.
    A **NR-6** define a obrigatoriedade do fornecimento e uso correto dos EPIs. Já a **NR-12** trata da segurança em
    máquinas e equipamentos, sendo uma das NRs mais fiscalizadas do país.  

    ## 📌 Por que segurança é um dever ético e não apenas legal?
    - Porque protege não só o operador, mas sua família e sua qualidade de vida
    - Reduz lesões permanentes, afastamentos e sequelas
    - Constrói um ambiente de confiança e cultura preventiva
    - Reduz custos invisíveis e evita multas e indenizações

    ## 📜 Normas mais aplicadas neste contexto
    - NR-6 — Equipamentos de Proteção Individual
    - NR-12 — Máquinas e Equipamentos
    - NR-17 — Ergonomia
    - NR-35 — Trabalho em Altura

    ## ⚠ Exemplos reais
    - Amputações por falha em enclausuramento de máquinas (NR-12)
    - Perda auditiva por ausência de EPI (NR-6)
    - Lesão por esforço repetitivo por condições inadequadas (NR-17)
    - Queda de plataforma por falha em treinamento (NR-35)

    ## 🧠 Base Técnica / Fontes
    - FUNDACENTRO
    - MTE – Manuais de Aplicação das NR
    - Revista Proteção Industrial (2022)
    - Artigo: “Impacto da cultura de segurança na performance operacional”

    > Ética industrial significa não aceitar acidentes como “normais”, e sim buscar tolerância zero a riscos.
    """)

    elif topico == "Compliance":
    st.markdown("""
    Compliance no ambiente industrial significa “agir em conformidade” com leis, regulamentos internos, padrões de ética
    e valores institucionais. Ele garante integridade nas relações, transparência nos processos e proteção à empresa
    contra riscos legais e reputacionais.

    ## 📌 Não existe cultura ética sem compliance.
    O cumprimento da lei não é opcional — é obrigatório e representa respeito às pessoas, à empresa e à sociedade.

    ## ⚖ Base Legal
    - Lei 12.846/2013 (Lei Anticorrupção)
    - Decreto 8.420/2015 (Regulamentação)
    - ISO 37001 – Sistema de gestão antissuborno
    - Código Penal Brasileiro
    - LGPD (Lei Geral de Proteção de Dados)

    ## 🧩 Exemplos práticos de compliance industrial:
    - Proibição de “jeitinho” para liberar produção irregular
    - Envio de relatórios de qualidade sem adulteração
    - Proibição de corrupção interna ou pagamento de vantagens
    - Imparcialidade em promoções e avaliações
    - Rastreabilidade na cadeia produtiva

    ## ⚠ Riscos reais sem compliance:
    - Multas milionárias
    - Prisão de colaboradores e gestores
    - Interdição da fábrica
    - Perda de contratos internacionais
    - Danos irreversíveis à marca

    ## 🧠 Base Técnica / Fontes
    - CGU – Cartilha de Compliance
    - FGV – Estudos em integridade corporativa
    - Harvard Business Review (2021) – Compliance Culture

    > Compliance não é “moda”: é sobrevivência ética e legal da organização.
    """)
    elif topico == "Boas Práticas":
    st.markdown("""
    Boas práticas industriais englobam comportamento, organização, disciplina operacional, ética e respeito aos padrões
    estabelecidos. Um operador ético executa processos conforme especificado mesmo quando ninguém está olhando.

    ## 💡 Boas práticas envolvem:
    - Uso adequado de EPIs
    - Seguir padrões operacionais (POPs)
    - Manter a organização do posto de trabalho (5S)
    - Reportar falhas imediatamente
    - Respeitar equipamentos e recursos da empresa
    - Técnica + ética = execução confiável

    ## 🏭 Fundamentos Lean aplicados a ética
    - 5S
    - Kaizen
    - Jidoka (parar quando há anomalia)
    - Poka-Yoke (prevenção de erro)
    - Takt Time / Fluxo contínuo
    - Trabalho padronizado

    ## 📌 Exemplos de boas práticas:
    - Não ignorar falhas para “bater meta”
    - Não suprimir proteções de máquinas
    - Não alterar parâmetros sem autorização
    - Limpeza após o turno
    - Registro honesto de defeitos

    ## 🧠 Base Técnica / Fontes
    - Toyota Production System
    - Kaoru Ishikawa
    - Seiichi Nakajima (TPM)
    - Womack & Jones (Lean Thinking)

    > Boas práticas ≠ só seguir regras. Elas formam o caráter operacional do colaborador.
    """)

    elif topico == "Assédio Moral e Sexual":
    st.markdown("""
    Assédio é qualquer comportamento indesejado e reiterado que causa constrangimento, humilhação, intimidação ou
    constrói um ambiente hostil. É uma violação grave dos direitos humanos e da ética organizacional.

    ## Tipos mais comuns de assédio:
    - Moral (humilhações, isolamento, ameaças, xingamentos)
    - Sexual (convites, toques, chantagens, exposição, piadas)
    - Organizacional (pressão abusiva, metas impossíveis, punição pública)

    ## ⚖ Base Legal
    - Consolidação das Leis do Trabalho (CLT)
    - Código Penal Brasileiro – Art. 216-A
    - Lei 14.457/22 – Medidas de prevenção ao assédio
    - NR-17 (Ambiente psicologicamente saudável)
    - OIT – Convenção 190

    ## ⚠ Exemplos reais:
    - Gestor que expõe funcionário publicamente
    - Colega fazendo piadas de cunho sexual repetidamente
    - Pressão para “conceder favores” em troca de promoção
    - Apelidos constrangedores

    ## 🚨 Consequências
    - Demissão por justa causa
    - Indenização e danos morais
    - Processo criminal
    - Responsabilidade civil da empresa
    - Traumas psicológicos e suicídio

    > Onde existe respeito, existe segurança psicológica — base da ética industrial.
    """)

    elif topico == "Normas Regulamentadoras (NRs)":
    st.markdown("""
    As Normas Regulamentadoras (NRs) são leis federais emitidas pelo Ministério do Trabalho
    que estabelecem requisitos mínimos obrigatórios para proteger a saúde e a integridade dos trabalhadores.

    ## As NRs representam:
    - obrigação legal
    - diretriz técnica
    - compromisso ético com a vida
    - responsabilidade civil e criminal

    ## 📜 Principais NRs aplicadas à indústria:
    - NR-1 – Disposições gerais
    - NR-5 – CIPA
    - NR-6 – EPIs
    - NR-10 – Eletricidade
    - NR-12 – Máquinas e equipamentos
    - NR-17 – Ergonomia
    - NR-26 – Sinalização
    - NR-35 – Trabalho em altura

    ## 📌 Aplicação ética das NRs:
    - Cumprir procedimentos mesmo sem fiscalização
    - Não mascarar condições inseguras
    - Parar máquina quando há risco
    - Realizar treinamentos com responsabilidade

    ## ⚠ Exemplos reais:
    - Multa + interdição por NR-12 em injetoras
    - Queda fatal em plataforma sem NR-35
    - Choque elétrico por falha NR-10

    ## 🧠 Fontes técnicas:
    - Fundacentro
    - MTE
    - ABNT
    - Estudos da USP sobre gestão de riscos industriais

    > NRs não são burocracia — são a diferença entre vida e morte.
    """)

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
