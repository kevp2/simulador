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
            "incluindo dispositivos de bloqueio (lockout/tagout) e intertravamentos."
        ),
        "questoes": [
            {"pergunta": "De acordo com a NR-6, qual a ação correta ao identificar um EPI danificado?",
             "opcoes": ["Consertar sozinho e usar", "Comunicar e aguardar substituição", "Continuar sem EPI"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Consertar sozinho é perigoso.",
                 "Correto: Comunicar e aguardar substituição é ético e seguro.",
                 "Errado: Continuar sem EPI viola normas."]},
            {"pergunta": "Ao operar uma máquina sem proteção adequada, o operador está:",
             "opcoes": ["Cumprindo a NR-12", "Violando normas e ética", "Aumentando produtividade legalmente"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Cumprir a NR-12 exige proteção.",
                 "Correto: Operar sem proteção viola norma e ética.",
                 "Errado: Não é legal nem seguro."]},
            {"pergunta": "Participar de treinamentos de segurança é:",
             "opcoes": ["Opcional", "Obrigatório e ético", "Perda de tempo"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é opcional.",
                 "Correto: Treinamentos são obrigatórios e reforçam ética.",
                 "Errado: Não é perda de tempo."]},
            {"pergunta": "O que deve ser feito ao identificar risco de acidente?",
             "opcoes": ["Ignorar se não afetar você", "Reportar imediatamente", "Apenas observar"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Ignorar é antiético.",
                 "Correto: Reportar imediatamente é procedimento correto.",
                 "Errado: Apenas observar não previne acidente."]},
            {"pergunta": "Bloquear uma máquina durante manutenção é:",
             "opcoes": ["Irrelevante", "Exigência da NR-12", "Opcional se estiver com pressa"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é irrelevante.",
                 "Correto: Bloqueio é exigência da NR-12.",
                 "Errado: Nunca opcional."]},
            {"pergunta": "Usar EPI de forma inadequada pode resultar em:",
             "opcoes": ["Acidentes e penalidades", "Nada acontece", "Recomendação de produção"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Uso inadequado pode gerar acidentes e punições.",
                 "Errado: Algo pode acontecer sim.",
                 "Errado: Não é recomendação de produção."]},
            {"pergunta": "NR-12 estabelece que proteções em máquinas devem ser:",
             "opcoes": ["Sempre removíveis para agilizar operação", "Fixas e seguras", "Ignoradas se operador for experiente"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Nunca removíveis apenas para agilizar.",
                 "Correto: Proteções devem ser fixas e seguras.",
                 "Errado: Não devem ser ignoradas."]},
            {"pergunta": "Se houver dúvida sobre segurança, o operador deve:",
             "opcoes": ["Adivinhar procedimento", "Consultar manual ou supervisor", "Ignorar o risco"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Adivinhar é inseguro.",
                 "Correto: Consultar manual ou supervisor é seguro.",
                 "Errado: Ignorar risco é antiético."]},
            {"pergunta": "Cumprir procedimentos de bloqueio é:",
             "opcoes": ["Opcional para operadores experientes", "Obrigatório e ético", "Desnecessário"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Nunca opcional.",
                 "Correto: Cumprimento é obrigatório e ético.",
                 "Errado: Não é desnecessário."]},
            {"pergunta": "Reportar quase acidentes contribui para:",
             "opcoes": ["Prevenção de futuros acidentes", "Nada", "Somente punição de colegas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Ajuda a prevenir acidentes futuros.",
                 "Errado: Tem impacto real.",
                 "Errado: Não é para punir colegas."]}
        ]
    },
    "Boas práticas": {
        "conteudo": (
            "Boas práticas industriais incluem organização, limpeza, padronização e comunicação eficiente. "
            "Seguir 5S, realizar checklists, reportar não conformidades, manter áreas limpas e organizar materiais garantem segurança, eficiência e ética no trabalho."
        ),
        "questoes": [
            {"pergunta": "Manter área limpa e organizada é:",
             "opcoes": ["Opcional", "Obrigatório", "Desnecessário"],
             "resposta": 1,
             "explicacao": [
                 "Errado: Não é opcional.",
                 "Correto: É obrigatório e ético.",
                 "Errado: Não é desnecessário."]},
            {"pergunta": "Reportar não conformidades é:",
             "opcoes": ["Obrigatório", "Opcional", "Desnecessário"],
             "resposta": 0,
             "explicacao": [
                 "Correto: É obrigação ética e legal.",
                 "Errado: Não é opcional.",
                 "Errado: Não é desnecessário."]},
            {"pergunta": "Seguir procedimentos padronizados garante:",
             "opcoes": ["Segurança e qualidade", "Apenas rapidez", "Nada"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Segurança e qualidade são garantidas.",
                 "Errado: Não é só rapidez.",
                 "Errado: Tem impacto real."]},
            {"pergunta": "Checklist diário serve para:",
             "opcoes": ["Organizar tarefas e prevenir erros", "Aumentar burocracia", "Ignorar problemas"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Ajuda a prevenir erros.",
                 "Errado: Não é burocracia sem sentido.",
                 "Errado: Não se deve ignorar problemas."]},
            {"pergunta": "Comunicação eficiente evita:",
             "opcoes": ["Acidentes e retrabalho", "Somente fofocas", "Nada"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Evita acidentes e retrabalho.",
                 "Errado: Não se limita a fofocas.",
                 "Errado: Impacto real existe."]},
            {"pergunta": "Armazenar materiais corretamente garante:",
             "opcoes": ["Segurança", "Não importa", "Perda de tempo"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Garante segurança.",
                 "Errado: Importa sim.",
                 "Errado: Não é perda de tempo."]},
            {"pergunta": "Participar de reuniões de 5S é:",
             "opcoes": ["Obrigatório", "Opcional", "Irrelevante"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Ajuda na implementação ética e correta do 5S.",
                 "Errado: Não é opcional.",
                 "Errado: Não é irrelevante."]},
            {"pergunta": "Sinalizar áreas de risco é:",
             "opcoes": ["Obrigatório", "Opcional", "Nunca necessário"],
             "resposta": 0,
             "explicacao": [
                 "Correto: É exigência ética e legal.",
                 "Errado: Não é opcional.",
                 "Errado: Nunca necessário é incorreto."]},
            {"pergunta": "Padronização de processos ajuda a:",
             "opcoes": ["Reduzir erros e acidentes", "Só velocidade", "Nada"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Reduz erros e acidentes.",
                 "Errado: Não é só velocidade.",
                 "Errado: Tem impacto real."]},
            {"pergunta": "Feedback construtivo é:",
             "opcoes": ["Importante e ético", "Desnecessário", "Prejudicial"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Melhora desempenho e ética.",
                 "Errado: Não é desnecessário.",
                 "Errado: Não é prejudicial."]}
        ]
    },
    "Compliance": {
        "conteudo": (
            "Compliance é a prática de seguir normas legais, políticas internas e ética corporativa. "
            "Inclui prevenção de fraudes, uso correto de recursos, transparência em processos e conduta ética de todos os colaboradores."
        ),
        "questoes": [
            {"pergunta": "O que é compliance?",
             "opcoes": ["Cumprimento de normas e ética", "Ignorar regras", "Somente financeiro"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Envolve normas e ética.",
                 "Errado: Ignorar regras é antiético.",
                 "Errado: Não se limita a finanças."]},
            {"pergunta": "Denunciar irregularidades é:",
             "opcoes": ["Obrigatório e ético", "Opcional", "Errado"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Obrigatório para manter compliance.",
                 "Errado: Não é opcional.",
                 "Errado: Não é errado."]},
            {"pergunta": "Uso de recursos da empresa para fins pessoais é:",
             "opcoes": ["Violação de compliance", "Aceitável", "Recomendado"],
             "resposta": 0,
             "explicacao": [
                 "Correto: É violação.",
                 "Errado: Não é aceitável.",
                 "Errado: Nunca recomendado."]},
            {"pergunta": "Assinatura de documentos falsos:",
             "opcoes": ["É fraude", "É normal", "Não importa"],
             "resposta": 0,
             "explicacao": [
                 "Correto: É fraude.",
                 "Errado: Não é normal.",
                 "Errado: Importa sim."]},
            {"pergunta": "Transparência em processos ajuda a:",
             "opcoes": ["Evitar corrupção", "Esconder problemas", "Nada"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Evita corrupção e problemas legais.",
                 "Errado: Esconder é antiético.",
                 "Errado: Tem impacto real."]},
            {"pergunta": "Treinamentos de ética são:",
             "opcoes": ["Obrigatórios", "Desnecessários", "Somente opcionais"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Devem ser realizados por todos.",
                 "Errado: Não são desnecessários.",
                 "Errado: Não apenas opcionais."]},
            {"pergunta": "Conflitos de interesse devem ser:",
             "opcoes": ["Reportados imediatamente", "Escondidos", "Ignorados"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Devem ser reportados.",
                 "Errado: Não se escondem.",
                 "Errado: Não se ignoram."]},
            {"pergunta": "Presentes de fornecedores devem ser:",
             "opcoes": ["Reportados conforme política", "Aceitos sempre", "Negados sem registrar"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Devem ser reportados.",
                 "Errado: Nem sempre aceitos.",
                 "Errado: Negar não basta."]},
            {"pergunta": "Sigilo de informações é:",
             "opcoes": ["Obrigatório", "Opcional", "Irrelevante"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Obrigatório por compliance.",
                 "Errado: Não é opcional.",
                 "Errado: Não é irrelevante."]},
            {"pergunta": "Compliance visa:",
             "opcoes": ["Integridade e ética", "Aumentar lucro apenas", "Ignorar leis"],
             "resposta": 0,
             "explicacao": [
                 "Correto: Visa integridade e ética.",
                 "Errado: Não é só lucro.",
                 "Errado: Não ignora leis."]}
        ]
    },
    "Assédio Moral e Sexual": {
        "conteudo": (
            "Assédio moral é qualquer ação que humilhe ou constranja o trabalhador repetidamente. "
            "Assédio sexual é qualquer comportamento com conotação sexual não desejado. Ambos são proibidos por lei e políticas internas."
        ),
        "questoes": [
            {"pergunta": "Assédio moral é:",
             "opcoes": ["Humilhação repetida", "Feedback construtivo", "Brincadeira leve"], 
             "resposta": 0,
             "explicacao": ["Correto: Humilhação repetida.", "Errado: Feedback construtivo não é assédio.", "Errado: Brincadeira leve não caracteriza assédio."]},
            {"pergunta": "Assédio sexual é:",
             "opcoes": ["Comportamento sexual não desejado", "Elogio profissional", "Amizade entre colegas"], 
             "resposta": 0,
             "explicacao": ["Correto: Qualquer comportamento sexual não desejado.", "Errado: Elogio profissional não é assédio.", "Errado: Amizade não é assédio."]},
            {"pergunta": "Denunciar assédio é:",
             "opcoes": ["Obrigatório e protegido", "Errado", "Opcional"], 
             "resposta": 0,
             "explicacao": ["Correto: Denúncias são protegidas.", "Errado: Não é errado denunciar.", "Errado: Não é opcional."]},
            {"pergunta": "Um chefe que insiste em elogios sexuais é:",
             "opcoes": ["Assediador", "Amigável", "Neutro"], 
             "resposta": 0,
             "explicacao": ["Correto: É assédio sexual.", "Errado: Não é amigável.", "Errado: Não é neutro."]},
            {"pergunta": "Piadas de teor sexual repetidas no ambiente:",
             "opcoes": ["Assédio", "Humor aceitável", "Inofensivo"], 
             "resposta": 0,
             "explicacao": ["Correto: É assédio sexual.", "Errado: Não é humor aceitável.", "Errado: Não é inofensivo."]},
            {"pergunta": "Ignorar assédio é:",
             "opcoes": ["Inadequado", "Aceitável", "Recomendado"], 
             "resposta": 0,
             "explicacao": ["Correto: Ignorar é inadequado.", "Errado: Não é aceitável.", "Errado: Não é recomendado."]},
            {"pergunta": "Conselhos sobre vestimenta sexualizada no trabalho:",
             "opcoes": ["Podem configurar assédio", "São instruções normais", "Não têm impacto"], 
             "resposta": 0,
             "explicacao": ["Correto: Pode configurar assédio.", "Errado: Não é instrução normal.", "Errado: Tem impacto real."]},
            {"pergunta": "Exigir favores sexuais:",
             "opcoes": ["É crime", "É opção do funcionário", "Não tem consequências"], 
             "resposta": 0,
             "explicacao": ["Correto: É crime.", "Errado: Não é opção.", "Errado: Tem consequências legais."]},
            {"pergunta": "Assédio moral pode incluir:",
             "opcoes": ["Isolamento e humilhação", "Treinamento normal", "Orientação"], 
             "resposta": 0,
             "explicacao": ["Correto: Isolamento e humilhação.", "Errado: Treinamento não é assédio.", "Errado: Orientação não é assédio."]},
            {"pergunta": "Boas práticas para evitar assédio:",
             "opcoes": ["Respeito, denúncia e conscientização", "Ignorar tudo", "Rir das piadas"], 
             "resposta": 0,
             "explicacao": ["Correto: Respeito e denúncia.", "Errado: Ignorar não ajuda.", "Errado: Rir não ajuda."]}
        ]
    },
    "Normas Regulamentadoras": {
        "conteudo": (
            "Normas Regulamentadoras (NRs) são regras do Ministério do Trabalho que garantem segurança, saúde e direitos do trabalhador. "
            "Incluem NR-6 (EPIs), NR-12 (máquinas), NR-5 (CIPA), NR-10 (eletricidade) e NR-9 (PPRA)."
        ),
        "questoes": [
            {"pergunta": "NR-6 trata de:",
             "opcoes": ["EPIs", "Máquinas", "CIPA"], 
             "resposta": 0,
             "explicacao": ["Correto: EPIs.", "Errado: Não é máquinas.", "Errado: Não é CIPA."]},
            {"pergunta": "NR-12 trata de:",
             "opcoes": ["Segurança de máquinas", "EPIs", "Eletricidade"], 
             "resposta": 0,
             "explicacao": ["Correto: Segurança de máquinas.", "Errado: Não EPIs.", "Errado: Não eletricidade."]},
            {"pergunta": "NR-5 estabelece:",
             "opcoes": ["CIPA", "Treinamentos gerais", "PPRA"], 
             "resposta": 0,
             "explicacao": ["Correto: CIPA.", "Errado: Não treinamentos gerais.", "Errado: Não PPRA."]},
            {"pergunta": "NR-10 trata de:",
             "opcoes": ["Segurança em eletricidade", "EPIs", "Máquinas"], 
             "resposta": 0,
             "explicacao": ["Correto: Segurança elétrica.", "Errado: Não EPIs.", "Errado: Não máquinas."]},
            {"pergunta": "NR-9 é sobre:",
             "opcoes": ["PPRA", "CIPA", "EPI"], 
             "resposta": 0,
             "explicacao": ["Correto: PPRA.", "Errado: Não CIPA.", "Errado: Não EPI."]},
            {"pergunta": "Cumprir NRs é:",
             "opcoes": ["Obrigatório", "Opcional", "Irrelevante"], 
             "resposta": 0,
             "explicacao": ["Correto: Obrigatório.", "Errado: Não opcional.", "Errado: Não irrelevante."]},
            {"pergunta": "NR-12 exige proteção de máquinas:",
             "opcoes": ["Sempre", "Às vezes", "Nunca"], 
             "resposta": 0,
             "explicacao": ["Correto: Sempre.", "Errado: Não às vezes.", "Errado: Nunca."]},
            {"pergunta": "NR-6 exige fornecimento de EPI:",
             "opcoes": ["Pelo empregador", "Pelo funcionário", "Não exige"], 
             "resposta": 0,
             "explicacao": ["Correto: Pelo empregador.", "Errado: Não funcionário.", "Errado: Não é opcional."]},
            {"pergunta": "NR-5 envolve:",
             "opcoes": ["Formação da CIPA", "EPIs", "NR-10"], 
             "resposta": 0,
             "explicacao": ["Correto: CIPA.", "Errado: Não EPIs.", "Errado: Não NR-10."]},
            {"pergunta": "NR-9 exige:",
             "opcoes": ["PPRA documentado", "Treinamento isolado", "Somente EPI"], 
             "resposta": 0,
             "explicacao": ["Correto: PPRA documentado.", "Errado: Não treinamento isolado.", "Errado: Não só EPI."]}
        ]
    }
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

# ---------- TÓPICOS ----------
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
            save_user_data(st.session_state["user"]["email"], {
                "topic": topic_name,
                "pergunta": q["pergunta"],
                "escolha": choice,
                "correta": q["opcoes"][correta_idx]
            })

# ---------- ADMIN ----------
def admin_panel():
    st.header("Painel de Administração")
    st.write("Somente visível para administrador.")
    all_files = DATA_DIR.glob("*.json")
    df_all = []
    for f in all_files:
        data = json.loads(f.read_text(encoding='utf-8'))
        for h in data.get("history", []):
            h["usuario"] = f.name.replace("_at_", "@").replace(".json", "")
            df_all.append(h)
    if df_all:
        df = pd.DataFrame(df_all)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Exportar CSV", csv, "dados.csv", "text/csv")
        acertos = df.apply(lambda x: x["escolha"] == x["correta"], axis=1).sum()
        erros = len(df) - acertos
        fig, ax = plt.subplots()
        ax.pie([acertos, erros], labels=["Acertos", "Erros"], autopct='%1.1f%%', colors=["green","red"])
        st.pyplot(fig)
    else:
        st.info("Nenhum dado registrado ainda.")

# ---------- MAIN ----------
def main():
    st.sidebar.title("Simulador Ético Industrial")
    if "user" not in st.session_state:
        login_screen()
        return
    st.sidebar.write(f"Logado como: {st.session_state['user']['email']}")
    if st.sidebar.button("Logout"):
        st.session_state.pop("user")
        st.experimental_rerun()
    menu = list(TOPICOS.keys())
    if st.session_state["user"]["email"] == ADMIN_EMAIL:
        menu.append("Administração")
    choice = st.sidebar.selectbox("Escolha um tópico", menu)
    if choice == "Administração":
        admin_panel()
    else:
        show_topic(choice)

if __name__ == "__main__":
    main()
