# 🏥 Medical RAG - Prática de Qdrant & vLLM

Bem-vindo à prática do **Capítulo 2 (CH2)**!

O objetivo deste laboratório é dominar duas tecnologias fundamentais para IA moderna: **Bancos Vetoriais (Qdrant)** e **Inferência de LLMs (Llama.cpp/vLLM)**.

Para isso, construímos uma aplicação de demonstração: um **Assistente Médico com RAG**.

![Badge](https://img.shields.io/badge/Focus-Vector%20Database%20%26%20Local%20LLM-blueviolet)

---

## 🎯 O que você vai aprender?

O "Chat Médico" é apenas o meio para aprendermos o fim:

1. **Qdrant (Vector Database)**:
    * Como armazenar texto em formato de números (embeddings).
    * Como fazer buscas por *significado* (Busca Semântica) e não por palavras-chave.
2. **LLM Local (vLLM / Llama.cpp)**:
    * Como rodar uma Inteligência Artificial (como o Qwen2.5) no **seu próprio servidor/PC**, sem pagar API da OpenAI.
    * Entender o custo computacional e latência.

---

## 🚀 Como Rodar

Pré-requisito: **Docker Desktop** instalado.

1. **Limpar ambiente anterior**:

    ```bash
    docker compose down -v
    ```

2. **Iniciar a Aplicação**:

    ```bash
    docker compose up --build
    ```

    > **Aguarde**: O sistema baixará o modelo de IA (~1.5GB).

3. **Acessar**:
    👉 **[http://localhost:8080](http://localhost:8080)**

---

## Explorando as Tecnologias

Use a aplicação para "ver" o Qdrant e o LLM trabalhando:

### 1. Testando o Qdrant (A Memória)

1. Vá na aba **"Base de Conhecimento"** e envie um PDF ou texto.
    * *O que acontece?* O texto é quebrado, convertido em vetores pelo `FastEmbed` e indexado no **Qdrant**.
2. Vá no Chat e pergunte algo sobre o texto.
3. Olhe o **Painel de Debug (Direita)**:
    * Veja o **"Contexto Recuperado"**. Esses são os trechos que o **Qdrant** achou mais similares matematicamente à sua pergunta.

### 2. Testando o LLM Local (O Cérebro)

1. Ainda no Painel de Debug, veja o **"Prompt Construído"**.
    * Nós "colamos" o texto do Qdrant dentro do prompt do modelo.
2. A resposta que aparece no chat é gerada 100% localmente pelo container `ch2-llm`.

---

## 🏗️ Arquitetura: Quem faz o quê?

### 🧠 LLM Service (`ch2-llm`)

* **O que é**: Um servidor Python rodando `Llama.cpp`.
* **Papel**: Substitui o GPT-4. Recebe texto e completa o texto.
* **Modelo**: Usamos o `Qwen2.5-1.5B-Instruct` (leve e rápido para CPU).

### 💾 Qdrant (`ch2-qdrant`)

* **O que é**: Um banco de dados especializado em vetores de alta dimensão.
* **Papel**: É a "memória de longo prazo". Permite que o LLM "leia" documentos que ele não conhecia durante o treinamento.

### ⚙️ API (`ch2-api`)

* **Papel**: O orquestrador.
    1. Recebe a pergunta.
    2. Vai no **Qdrant** buscar ajuda.
    3. Manda tudo pro **LLM**.
    4. Devolve pro usuário.

---

## ⚠️ Dica de Estudo

Se você quer ver como conectamos o Python ao Qdrant, abra `app/services.py` e procure a classe `VectorDbService`. Lá está o código cru de conexão e busca.
