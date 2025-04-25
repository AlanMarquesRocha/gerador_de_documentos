import streamlit as st
import os
import requests
from langchain_community.llms import OpenAI
from langchain_pipeline.utils import salvar_contrato_pdf
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from validate_docbr import CPF, CNPJ

# Carrega variáveis de ambiente e inicializa validadores
load_dotenv()

# Substitua sua OPENAI_API_KEY no arquivo .env
api_key = os.getenv("OPENAI_API_KEY")
cpf_validator = CPF()
cnpj_validator = CNPJ()

# Configura LLM e prompt que será utilizado
llm = OpenAI(temperature = 0.5, max_tokens = 1000, openai_api_key = api_key)
template = """
Gere um contrato completo de prestação de serviços com os seguintes dados:

CONTRATANTE:
- Nome: {contratante_nome}
- Nacionalidade: {contratante_nacionalidade}
- Estado civil: {contratante_estado_civil}
- CPF: {contratante_cpf}
- RG: {contratante_rg}
- Endereço: {contratante_endereco}

CONTRATADO:
- Nome / Razão Social: {contratado_nome}
- CNPJ: {contratado_cnpj}
- Representante legal: {contratado_representante}
- CPF do representante: {contratado_cpf}
- RG do representante: {contratado_rg}
- Endereço: {contratado_endereco}

OBJETO DO CONTRATO:
{objeto}

O contrato deve conter:
1. Preâmbulo com identificação das partes
2. Cláusulas formais (mínimo 5)
3. Redação jurídica com tom formal
4. Cláusula de foro
5. Espaço para assinaturas

O contrato deve estar no padrão jurídico brasileiro.
"""
prompt = PromptTemplate(
    input_variables = [
        "contratante_nome", "contratante_nacionalidade", "contratante_estado_civil",
        "contratante_cpf", "contratante_rg", "contratante_endereco",
        "contratado_nome", "contratado_cnpj", "contratado_representante",
        "contratado_cpf", "contratado_rg", "contratado_endereco",
        "objeto", "valor", "duracao", "jurisdicao"
    ],
    template = template
)
chain = LLMChain(llm = llm, prompt = prompt)

# Configuração da página do gerador de contrato de prestação de serviços
st.set_page_config(page_title = "Gerador de Contratos", layout = "centered")
st.title("📄 Gerador de Contrato de Prestação de Serviços")

# Formulário dividido em seções expandidas
with st.expander("🔷 Informações do Contratante", expanded = False):
    contratante_nome = st.text_input("Nome completo:", key = "contratante_nome")
    nacionalidades = ["Escolha uma opção", "Brasileiro", "Estrangeiro", "Naturalizado"]
    contratante_nacionalidade = st.selectbox("Nacionalidade:", nacionalidades, key = "contratante_nacionalidade")
    estados_civis = ["Escolha uma opção", "Solteiro", "Casado", "Divorciado", "Viúvo", "União Estável", "Outro"]
    contratante_estado_civil = st.selectbox("Estado Civil:", estados_civis, key = "contratante_estado_civil")
    contratante_cpf = st.text_input("CPF (000.000.000-00):", key = "contratante_cpf")
    contratante_rg = st.text_input("RG:", key = "contratante_rg")
    # CEP e endereço
    contratante_cep = st.text_input("CEP (00000000):", key="contratante_cep")
    if st.button("🔎 Buscar CEP", key="btn_cep_contratante"):
        if contratante_cep:
            res = requests.get(f"https://viacep.com.br/ws/{contratante_cep}/json/")
            if res.ok and "erro" not in res.json():
                data = res.json()
                st.session_state.rua = data["logradouro"]
                st.session_state.bairro = data["bairro"]
                st.session_state.cidade = data["localidade"]
                st.session_state.estado = data["uf"]
            else:
                with st.modal("CEP Inválido!!"):
                    st.error("CEP não encontrado. Verifique o número e tente novamente.")
    contratante_rua = st.text_input("Rua:", value = st.session_state.get("rua", ""), key = "contratante_rua")
    contratante_bairro = st.text_input("Bairro:", value = st.session_state.get("bairro", ""), key = "contratante_bairro")
    contratante_cidade = st.text_input("Cidade:", value = st.session_state.get("cidade", ""), key = "contratante_cidade")
    contratante_estado = st.text_input("Estado:", value = st.session_state.get("estado", ""), key = "contratante_estado")
    contratante_numero = st.text_input("Número:", key = "contratante_numero")
    contratante_complemento = st.text_input("Complemento:", key = "contratante_complemento")

with st.expander("🔶 Informações do Contratado", expanded = False):
    contratado_nome = st.text_input("Razão Social / Nome:", key = "contratado_nome")
    contratado_cnpj = st.text_input("CNPJ (00.000.000/0000-00):",  key = "contratado_cnpj")
    contratado_representante = st.text_input("Nome do Representante:", key = "contratado_representante")
    contratado_cpf = st.text_input("CPF do Representante (000.000.000-00):", key = "contratado_cpf")
    contratado_rg = st.text_input("RG do Representante:", key = "contratado_rg")
    contratado_cep = st.text_input("CEP (00000000):", key = "contratado_cep")
    if st.button("🔎 Buscar CEP", key = "btn_cep_contratado"):
        if contratado_cep:
            res = requests.get(f"https://viacep.com.br/ws/{contratado_cep}/json/")
            if res.ok and "erro" not in res.json():
                data = res.json()
                st.session_state.rua_c = data["logradouro"]
                st.session_state.bairro_c = data["bairro"]
                st.session_state.cidade_c = data["localidade"]
                st.session_state.estado_c = data["uf"]
            else:
                with st.modal("CEP Inválido"):
                    st.error("CEP não encontrado. Verifique e tente novamente.")
    contratado_rua = st.text_input("Rua:", value = st.session_state.get("rua_c", ""), key = "contratado_rua")
    contratado_bairro = st.text_input("Bairro:", value = st.session_state.get("bairro_c", ""), key = "contratado_bairro")
    contratado_cidade = st.text_input("Cidade:", value = st.session_state.get("cidade_c", ""), key = "contratado_cidade")
    contratado_estado = st.text_input("Estado:", value = st.session_state.get("estado_c", ""), key = "contratado_estado")
    contratado_numero = st.text_input("Número:", key = "contratado_numero")
    contratado_complemento = st.text_input("Complemento:", key = "contratado_complemento")

with st.expander("📋 Detalhes do Contrato", expanded = False):
    objeto = st.text_area("Objeto do Contrato:", key = "objeto")
    valor = st.text_input("Valor do Contrato:", key = "valor")
    duracao = st.text_input("Duração (meses):", key = "duracao")
    jurisdicao = st.text_input("Foro/Jurisdição:", key = "jurisdicao")

# Botão principal de geração
if st.button("📄 Gerar Contrato", type = "primary"):
    # Validações
    errors = []
    if not contratante_nome: errors.append("Informe o nome do Contratante.")
    if contratante_nacionalidade == "Escolha uma opção":
        errors.append("Selecione a nacionalidade.")
    if contratante_estado_civil == "Escolha uma opção":
        errors.append("Selecione o estado civil.")
    if not cpf_validator.validate(contratante_cpf):
        errors.append("CPF do Contratante inválido.")
    if not contratado_nome: errors.append("Informe o nome do Contratado.")
    if not cnpj_validator.validate(contratado_cnpj):
        errors.append("CNPJ inválido.")
    if errors:
        with st.modal("⚠️ Corrija os erros"):
            for e in errors:
                st.error(e)
        st.stop()

    # Combina endereços
    contra_end = f"{contratante_rua}, {contratante_numero}, {contratante_complemento}, {contratante_bairro}, {contratante_cidade} - {contratante_estado}"
    contd_end = f"{contratado_rua}, {contratado_numero}, {contratado_complemento}, {contratado_bairro}, {contratado_cidade} - {contratado_estado}"

    # Gera e mostra o contrato
    with st.spinner("Gerando contrato..."):
        contrato_gerado = chain.run({
            "contratante_nome": contratante_nome,
            "contratante_nacionalidade": contratante_nacionalidade,
            "contratante_estado_civil": contratante_estado_civil,
            "contratante_cpf": contratante_cpf,
            "contratante_rg": contratante_rg,
            "contratante_endereco": contra_end,
            "contratado_nome": contratado_nome,
            "contratado_cnpj": contratado_cnpj,
            "contratado_representante": contratado_representante,
            "contratado_cpf": contratado_cpf,
            "contratado_rg": contratado_rg,
            "contratado_endereco": contd_end,
            "objeto": objeto,
            "valor": valor,
            "duracao": duracao,
            "jurisdicao": jurisdicao
        })

        caminho_pdf = salvar_contrato_pdf(contrato_gerado)

        # Feedback de sucesso
        with st.modal("✅ Contrato Gerado"):
            st.success("Contrato gerado com sucesso!")
            st.download_button("📥 Baixar .txt", contrato_gerado, "contrato.txt", "text/plain")
            with open(caminho_pdf, "rb") as f:
                st.download_button("📄 Baixar PDF", f, os.path.basename(caminho_pdf), "application/pdf")
            st.text_area("Visualização", contrato_gerado, height = 300)

