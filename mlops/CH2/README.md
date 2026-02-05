# CH2 — Instanciando Modelos de Linguagem com vLLM e Bancos Vetoriais com Qdrant

Este capítulo aprofunda a construção de infraestruturas para aplicações baseadas em modelos de linguagem, abordando dois pilares essenciais para sistemas modernos de IA generativa: a execução eficiente de Large Language Models por meio do vLLM e o armazenamento e recuperação semântica de informações utilizando bancos vetoriais com Qdrant.

O foco principal está na transição de modelos experimentais para serviços reutilizáveis em produção, demonstrando como instanciar modelos de linguagem como serviços escaláveis e como integrar esses modelos a sistemas de busca vetorial para suportar aplicações como Retrieval-Augmented Generation, motores de recomendação semântica e assistentes inteligentes baseados em contexto.

Ao longo deste módulo, o participante irá compreender como estruturar um ambiente funcional para inferência de LLMs, como servir embeddings e como armazenar, indexar e recuperar vetores de forma eficiente, garantindo desempenho, escalabilidade e reprodutibilidade.

---

## O Papel dos Modelos de Linguagem em Sistemas de Produção

Modelos de linguagem de grande porte são cada vez mais utilizados para resolver problemas complexos de geração de texto, sumarização, question answering, classificação e automação de tarefas cognitivas. No entanto, a execução desses modelos em produção impõe desafios significativos relacionados a consumo de memória, latência, throughput e custo computacional.

vLLM é uma tecnologia projetada para otimizar a inferência de modelos de linguagem, permitindo o uso eficiente de GPU e o atendimento simultâneo de múltiplas requisições por meio de técnicas avançadas de gerenciamento de memória e cache. Ao utilizar vLLM, torna-se possível transformar um modelo de linguagem em um serviço de inferência escalável e adequado para ambientes de produção.

Neste capítulo, o modelo deixa de ser apenas um artefato de pesquisa e passa a operar como um serviço real, pronto para integração com APIs, pipelines e aplicações distribuídas.

---

## Bancos Vetoriais e Recuperação Semântica com Qdrant

Aplicações modernas de IA frequentemente dependem de recuperação semântica de informações, na qual textos, documentos ou outros tipos de dados são representados como vetores em um espaço de alta dimensionalidade. Esses vetores permitem consultas baseadas em similaridade semântica em vez de correspondência literal de palavras.

Qdrant é um banco vetorial projetado para armazenar, indexar e consultar embeddings de forma eficiente, suportando filtros, metadados e buscas aproximadas em larga escala. Ele é amplamente utilizado em arquiteturas de RAG, motores de busca inteligentes e sistemas de memória de longo prazo para agentes de IA.

Neste módulo, o participante aprenderá a instanciar um servidor Qdrant, inserir vetores gerados por modelos de embeddings, realizar consultas semânticas e integrar esse fluxo a modelos de linguagem para recuperação de contexto relevante.

---

## Integração entre LLMs e Bancos Vetoriais

A combinação entre modelos de linguagem e bancos vetoriais viabiliza arquiteturas capazes de responder perguntas com base em conhecimento externo, atualizar informações sem necessidade de retreinamento e reduzir alucinações por meio da recuperação de fontes relevantes.

Este capítulo demonstra como estruturar um pipeline no qual textos são convertidos em embeddings, armazenados no Qdrant e posteriormente recuperados para compor prompts enriquecidos enviados a um modelo servido via vLLM. Essa integração representa um dos padrões arquiteturais mais relevantes para sistemas de IA aplicados em produção.

---

## Estrutura do Capítulo

O conteúdo deste capítulo inclui scripts para execução de modelos de linguagem com vLLM, arquivos de configuração para inicialização do Qdrant, exemplos de ingestão de dados, geração de embeddings, inserção em banco vetorial e consultas semânticas. Também estão incluídos exemplos de integração entre os dois serviços, simulando um ambiente funcional de RAG.

Os exemplos foram projetados para serem reutilizados nos próximos capítulos, onde serão acoplados a APIs, microsserviços e pipelines automatizados.

---

## Ambiente e Pré-requisitos

Para executar os conteúdos deste capítulo, é esperado que o participante tenha Docker instalado e funcional, além de Python versão 3.9 ou superior. Recomenda-se o uso de GPU para execução eficiente dos modelos de linguagem, embora seja possível executar versões reduzidas em CPU para fins educacionais.

Também é necessário ter concluído o CH1 ou possuir familiaridade com conceitos de containerização e execução de serviços em containers.

---

## Quickstart: Preparando o Ambiente Local

O primeiro passo consiste em acessar a pasta correspondente ao capítulo CH2 dentro do repositório do workshop.

```bash
cd workshop-nlp-mlops/mlops/CH2
```

Caso ainda não tenha instalado as dependências do projeto, recomenda-se criar um ambiente virtual e instalar os pacotes necessários.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## Quickstart: Subindo o Qdrant Localmente

O Qdrant pode ser executado como um serviço local utilizando Docker, permitindo a criação de um banco vetorial pronto para uso.

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Após a inicialização, o serviço poderá ser acessado localmente por meio da API REST ou SDKs Python.

---

## Quickstart: Gerando Embeddings e Inserindo no Qdrant

Para gerar embeddings e armazená-los no banco vetorial, execute o script de ingestão incluído no capítulo.

```bash
python scripts/ingest_embeddings.py
```

Esse processo converte textos em vetores, cria uma coleção no Qdrant e insere os dados para posterior consulta semântica.

---

## Quickstart: Executando um Modelo de Linguagem com vLLM

O serviço de modelo de linguagem pode ser iniciado utilizando vLLM por meio do comando abaixo.

```bash
python services/start_vllm.py --model mistralai/Mistral-7B-Instruct
```

Após a inicialização, o modelo ficará disponível como um serviço de inferência local, pronto para receber requisições.

---

## Quickstart: Consultando o Banco Vetorial e Enriquecendo Prompts

Uma vez que os embeddings estejam armazenados e o modelo esteja em execução, é possível realizar consultas semânticas e enriquecer prompts automaticamente.

```bash
python examples/query_rag_pipeline.py
```

Esse script realiza uma busca no Qdrant com base na pergunta do usuário, recupera os documentos mais relevantes e injeta o conteúdo no prompt enviado ao modelo de linguagem, simulando um fluxo básico de Retrieval-Augmented Generation.

---

## Objetivo Prático do Capítulo

Ao final deste capítulo, o participante deverá ser capaz de instanciar um modelo de linguagem como serviço, operar um banco vetorial para armazenamento de embeddings e integrar ambos em um pipeline funcional de recuperação e geração de respostas. Também deverá compreender as implicações arquiteturais, computacionais e operacionais envolvidas na execução desses componentes em ambientes de produção.

Esse conhecimento é essencial para a construção de sistemas de IA escaláveis, capazes de lidar com grandes volumes de dados, múltiplos usuários e requisitos de desempenho em tempo real.

---

## Próximos Passos

Nos capítulos seguintes, os serviços de modelo de linguagem e banco vetorial criados neste módulo serão integrados a APIs públicas, arquiteturas de microsserviços, pipelines de orquestração e fluxos automatizados de CI/CD, aproximando cada vez mais o ambiente do workshop de cenários reais de produção.

