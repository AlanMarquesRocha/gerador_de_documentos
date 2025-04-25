# 📄 Gerador de Documentos Legais Personalizados com `LangChain`

Este projeto tem como objetivo automatizar a geração de documentos legais (como contratos, declarações e procurações) com o uso de **Modelos de Linguagem (LLMs)** integrados via **LangChain**. Basta preencher um formulário com as informações necessárias e o sistema gera um documento completo, pronto para uso.

---

## 🚀 Funcionalidades

- 📋 Formulário interativo para entrada de dados
- ⚙️ Geração automática de documentos jurídicos com base em prompts personalizados
- 📄 Exportação em formato `.pdf` e `.docx`
- 🧠 Utiliza LangChain + LLM (OpenAI ou outro provedor)
- 🌐 Interface web com Streamlit (ou FastAPI, a depender da versão)

---

## 📚 Modelos Suportados (Em breve novos modelos)

- Contrato de prestação de serviços

--- 

## ⚙️ Como Utilizar

1. **Clone o repositório:**  
   ```bash
   git clone https://github.com/AlanMarquesRocha/gerador_de_documentos.git
   cd gerador_de_documentos

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate (macOS/Linux)
   .venv\Scripts\activate (Windows)

3. **Instale as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

5. **Configure sua chave da OpenAI:** <br>
   Dentro de ``.env``, adicione:
   ```ini
   OPENAI_API_KEY=sk-...
   ```
   Mais informações sobre como configurar a chave da OpenAI, basta clicar [**aqui.**](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key?api-mode=responses)

6. **Execute a aplicação:** <br>
   Caso você esteja inicialmente utilizando uma IDE, execute no terminal:
    ```bash
      streamlit run app.py
    ```
8. **Gere seu docuemnto** <br>
Se tudo funcionar a imagem abaixo deverá aparecer:
<!-- Exibe a imagem reduzida em 70% (ou seja, 30% menor) -->
<img src="https://github.com/user-attachments/assets/5fda7a1a-dc46-451e-83da-cea89282c941" width="70%" alt="Imagem reduzida em 30%"/>


## 🧠 Tecnologias Utilizadas

- Python 3.10+
- [LangChain](https://www.langchain.com/)
- OpenAI API (ou outro backend LLM)
- Streamlit (interface)
- python-docx / fpdf2 (geração de documentos)
- GitHub Actions (CI/CD para builds automatizados)

---
