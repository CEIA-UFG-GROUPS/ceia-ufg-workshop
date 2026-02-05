# CH3 — Criando APIs para RAG e Arquiteturas de Microsserviços

Este capítulo aborda a transformação de pipelines de Inteligência Artificial em serviços consumíveis por aplicações reais, explorando a criação de APIs para sistemas baseados em Retrieval-Augmented Generation e a adoção de arquiteturas de microsserviços para garantir escalabilidade, modularidade e manutenibilidade em ambientes de produção.

O foco central está em converter os componentes desenvolvidos nos capítulos anteriores, como modelos de linguagem e bancos vetoriais, em serviços independentes, interoperáveis e prontos para integração com produtos digitais, aplicações web, chatbots, plataformas corporativas e fluxos automatizados.

Ao longo deste módulo, o participante compreenderá como estruturar APIs robustas para inferência de modelos, como expor pipelines de RAG como serviços web e como decompor sistemas de IA em microsserviços independentes, permitindo evolução contínua e operação em larga escala.

---

## APIs como Camada de Acesso a Sistemas de IA

Em ambientes de produção, modelos de Machine Learning raramente são utilizados de forma direta por usuários finais. Em vez disso, eles são encapsulados em serviços que expõem endpoints HTTP, permitindo que aplicações externas realizem inferências por meio de chamadas padronizadas.

A construção de APIs para IA envolve desafios específicos, incluindo controle de latência, validação de entrada, serialização de respostas, autenticação, versionamento e monitoramento. Neste capítulo, a API atua como uma camada intermediária entre o usuário e os componentes de inferência, garantindo que o modelo possa ser consumido de forma segura, escalável e previsível.

O framework FastAPI é utilizado como base para a implementação desses serviços, devido à sua eficiência, tipagem explícita, documentação automática e facilidade de integração com pipelines de Machine Learning.

---

## Retrieval-Augmented Generation como Serviço

Retrieval-Augmented Generation representa um padrão arquitetural no qual um modelo de linguagem é alimentado com contexto recuperado dinamicamente de um banco vetorial. Esse padrão permite que respostas sejam fundamentadas em dados externos atualizáveis, reduzindo dependência exclusiva do conhecimento interno do modelo.

Neste capítulo, o pipeline de RAG é transformado em um serviço completo, no qual uma requisição enviada à API dispara uma busca semântica no banco vetorial, recupera os documentos mais relevantes, constrói um prompt enriquecido e encaminha a solicitação para o modelo de linguagem, retornando ao usuário uma resposta contextualizada.

O objetivo é demonstrar como transformar um fluxo experimental em um endpoint confiável, capaz de atender múltiplos usuários simultaneamente.

---

## Arquiteturas de Microsserviços para Sistemas de IA

À medida que sistemas de IA crescem em complexidade, torna-se inviável manter todos os componentes em um único serviço monolítico. Arquiteturas de microsserviços permitem a separação de responsabilidades, possibilitando que serviços de inferência, recuperação de dados, autenticação, logging e monitoramento evoluam de forma independente.

Neste módulo, os serviços são organizados de forma distribuída, separando o servidor de modelo, o banco vetorial e a API de orquestração em componentes independentes que se comunicam por meio de protocolos HTTP ou mensageria. Essa abordagem favorece escalabilidade horizontal, tolerância a falhas e flexibilidade para atualizações futuras.

O participante aprenderá a estruturar uma aplicação de IA como um conjunto de serviços desacoplados, aproximando o ambiente do workshop de cenários reais utilizados em produção industrial.

---

## Estrutura do Capítulo

Este capítulo contém implementações de APIs REST para consumo de modelos de linguagem, exemplos de serviços RAG completos, arquivos Docker para empacotamento dos microsserviços, scripts de inicialização e exemplos de requisições para validação de funcionamento.

Os serviços desenvolvidos aqui são projetados para serem reutilizados nos próximos capítulos, onde serão integrados a infraestruturas de nuvem, pipelines automatizados e sistemas de orquestração.

---

## Ambiente e Pré-requisitos

Para acompanhar este capítulo, recomenda-se que o participante tenha concluído os capítulos anteriores ou possua familiaridade com execução de containers, modelos de linguagem e bancos vetoriais. É necessário ter Python versão 3.9 ou superior e Docker instalado e funcional.

Também é recomendado que o Qdrant e o serviço de modelo de linguagem configurados no CH2 estejam disponíveis localmente ou em ambiente remoto.

---

## Quickstart: Acessando o Diretório do Capítulo

O primeiro passo consiste em navegar até a pasta do CH3 dentro do repositório do workshop.

```bash
cd workshop-nlp-mlops/mlops/CH3
```

Caso ainda não exista um ambiente virtual configurado, recomenda-se criar um e instalar as dependências necessárias.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## Quickstart: Iniciando a API de RAG

A API principal do capítulo pode ser iniciada com o comando abaixo, que executa o serviço FastAPI responsável por orquestrar o fluxo de RAG.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Após a inicialização, a documentação interativa da API estará disponível no navegador.

```text
http://localhost:8000/docs
```

---

## Quickstart: Realizando uma Consulta ao Serviço RAG

Uma vez que a API esteja em execução, é possível enviar uma requisição para o endpoint responsável por gerar respostas baseadas em recuperação semântica.

```bash
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Explique o que é MLOps"}'
```

A resposta retornada incluirá conteúdo gerado pelo modelo de linguagem com base nos documentos recuperados do banco vetorial.

---

## Quickstart: Executando os Microsserviços via Docker Compose

Este capítulo inclui um arquivo docker-compose que permite subir todos os serviços de forma integrada, incluindo API, banco vetorial e servidor de modelo.

```bash
docker compose up --build
```

Após a inicialização, todos os serviços estarão disponíveis e conectados em uma arquitetura distribuída funcional.

---

## Objetivo Prático do Capítulo

Ao final deste capítulo, o participante deverá ser capaz de expor modelos de linguagem por meio de APIs REST, estruturar um pipeline completo de Retrieval-Augmented Generation como serviço e organizar sistemas de IA em uma arquitetura baseada em microsserviços.

Também deverá compreender como projetar serviços desacoplados, como lidar com comunicação entre componentes distribuídos e como preparar uma aplicação de IA para integração com sistemas reais em produção.

Esse conhecimento representa um passo essencial para a construção de plataformas escaláveis, robustas e prontas para ambientes corporativos e industriais.

---

## Próximos Passos

Nos próximos capítulos, os microsserviços desenvolvidos neste módulo serão integrados a infraestruturas baseadas em servidores e serverless, mecanismos de autoscaling e pipelines automatizados de CI/CD, elevando o ambiente do workshop para um nível próximo ao de sistemas de produção em larga escala.

