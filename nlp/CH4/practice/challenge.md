# 📖 README: Teoria e Desafios (RAG Educacional)

Bem-vindo à documentação teórica do nosso repositório de Retrieval-Augmented Generation (RAG). Este documento tem como objetivo explicar os conceitos por trás do código que você executou e propor desafios reais para evoluir essa arquitetura básica para um nível de produção.

## 🧠 A Teoria: Como nosso RAG funciona?

O padrão RAG foi criado para resolver dois grandes problemas dos Modelos de Linguagem (LLMs): **alucinações** (inventar fatos) e a **falta de conhecimento atualizado/privado**. Em vez de depender apenas do que o modelo aprendeu no treinamento, nós "pesquisamos" a resposta antes em uma base confiável e entregamos essa pesquisa para o LLM ler e formular a resposta final.

Nosso repositório divide esse fluxo em quatro pilares fundamentais:

### 1. Ingestão e Representação Semântica (Embeddings)

Computadores não entendem palavras, entendem números. Para que o nosso sistema saiba que "cachorro" e "cão" são conceitos próximos, transformamos nossos textos (o dataset SQuAD) em **Embeddings**.

* **O que fizemos:** Usamos o modelo `all-MiniLM-L6-v2` (pequeno e rápido para CPU) para converter cada parágrafo de texto em um vetor de 384 dimensões.

### 2. O Banco de Dados Vetorial (Qdrant)

Bancos de dados tradicionais (SQL) buscam por palavras-chave exatas. Bancos vetoriais buscam por **proximidade geométrica**.

* **O que fizemos:** Subimos uma instância do Qdrant via Docker e salvamos nossos vetores lá. Quando o usuário faz uma pergunta, transformamos a pergunta em vetor e pedimos ao Qdrant: *"Me dê os 3 vetores mais próximos (similares) a este aqui, usando a métrica de Distância de Cosseno"*.

### 3. Avaliação de Recuperação (Métricas)

Em um sistema RAG, se a busca falhar, o LLM vai falhar (ou alucinar). Por isso, precisamos medir a qualidade do nosso motor de busca usando métricas clássicas de Recuperação de Informação (IR):

* **Recall@k:** Dos documentos que importavam, quantos conseguimos trazer no nosso Top-K?
* **Precision@k:** Dos documentos que trouxemos no Top-K, quantos realmente eram úteis?
* **MRR (Mean Reciprocal Rank):** Quão no topo da lista estava o primeiro resultado correto?
* **NDCG:** Avalia a qualidade do ranqueamento como um todo, penalizando resultados corretos que aparecem muito para o final da lista.

### 4. Geração Aumentada (LLM)

A última etapa é a síntese. Pegamos os textos brutos que o Qdrant retornou e os empacotamos em um *Prompt* junto com a pergunta original do usuário.

* **O que fizemos:** Criamos uma instrução simples mandando o modelo atuar como um assistente, ler o contexto fornecido e responder à pergunta sem inventar dados.

---

## 🚀 Desafios para os Alunos: Evoluindo o Sistema

A versão atual deste repositório é intencionalmente ingênua. Ela funciona muito bem para textos curtos (como os parágrafos do SQuAD), mas falharia em cenários do mundo real (ex: ler PDFs inteiros, contratos de 50 páginas, etc.).

Sua missão é escolher um (ou mais) dos desafios abaixo e implementar no código-fonte!

### Nível 1: Melhorias Fundamentais

* **Desafio 1: Implementar *Chunking* (Fatiamento de Texto).** Atualmente, inserimos o parágrafo inteiro no banco. E se os documentos tivessem 10 páginas? O LLM estouraria o limite de tokens.
* *Sua tarefa:* Use bibliotecas como LangChain ou LlamaIndex para fatiar textos longos em pedaços de tamanho fixo (ex: 500 caracteres) com uma sobreposição (*overlap*) de 50 caracteres para não perder o contexto entre as quebras.

* **Desafio 2: Engenharia de Prompt Avançada.**
Nosso prompt atual é extremamente básico.
* *Sua tarefa:* Melhore o prompt no script `03_rag.py`. Adicione regras estritas (ex: *"Responda sempre em bullet points"*, *"Se a resposta não estiver no texto, responda EXATAMENTE: 'Informação não encontrada na base'"*). Adicione exemplos (*Few-Shot Prompting*) dentro da instrução.

### Nível 2: Otimização de Busca

* **Desafio 3: Busca Híbrida (Hybrid Search).**
A busca puramente semântica às vezes ignora nomes próprios ou siglas específicas.
* *Sua tarefa:* Pesquise sobre *Sparse Vectors* (como o BM25). Tente configurar o Qdrant para aceitar tanto a busca por embeddings (densa) quanto a busca por palavras-chave (esparsa) ao mesmo tempo.

* **Desafio 4: Adicionar um Re-Ranker (Cross-Encoder).**
Buscar muitos documentos é rápido, mas impreciso.
* *Sua tarefa:* Traga 10 resultados do Qdrant usando o modelo MiniLM rápido, mas adicione uma etapa intermediária usando um modelo mais pesado (Cross-Encoder, ex: `cross-encoder/ms-marco-MiniLM-L-6-v2`) para reordenar esses 10 resultados com alta precisão antes de enviar os 3 melhores para o LLM. Avalie como isso afeta o NDCG no script `02_metricas.py`!

### Nível 3: Arquitetura e Engenharia de Software

* **Desafio 5: Rodar 100% Local (Open Source).**
Atualmente o repositório consome a API paga da OpenAI.
* *Sua tarefa:* Substitua a chamada da OpenAI por uma requisição local. Use ferramentas como o **Ollama** ou **LM Studio** para rodar um modelo menor na sua máquina (ex: `Llama-3-8B`, `Phi-3`, ou `Gemma`) e consuma a API local dele no script.

* **Desafio 6: Streaming de Resposta na API.**
O FastAPI atual espera o LLM gerar o texto inteiro antes de devolver para o usuário.
* *Sua tarefa:* Modifique o endpoint `/rag` para utilizar *Server-Sent Events (SSE)* ou WebSockets, fazendo a resposta aparecer palavra por palavra na tela do usuário, igual ao ChatGPT.
