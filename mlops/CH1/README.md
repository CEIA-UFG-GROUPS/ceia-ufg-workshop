# CH1 — Introdução ao DevOps, MLOps e Containerização com Docker

Este capítulo apresenta os fundamentos necessários para compreender como sistemas modernos de Machine Learning e Inteligência Artificial são desenvolvidos, empacotados, distribuídos e operados em ambientes de produção. O foco está na convergência entre práticas de DevOps e MLOps, explorando como automação, reprodutibilidade, versionamento e infraestrutura como código se tornam pilares essenciais para a entrega confiável de soluções baseadas em modelos de aprendizado de máquina.

Ao longo deste módulo, o participante será introduzido aos conceitos que sustentam pipelines modernos de Machine Learning em produção, entendendo como o ciclo de vida de um modelo vai além do treinamento e envolve empacotamento, deploy, monitoramento, atualização e governança. Além disso, será abordado o papel da containerização como mecanismo fundamental para garantir portabilidade, isolamento e escalabilidade de aplicações.

---

## Contexto: DevOps e MLOps em Sistemas de IA

DevOps é um conjunto de práticas que busca integrar desenvolvimento de software e operações, reduzindo o tempo entre a escrita do código e sua execução em produção, ao mesmo tempo em que aumenta a confiabilidade e a qualidade do sistema entregue. Em ambientes de Inteligência Artificial, essa filosofia evolui para MLOps, que amplia o escopo ao incluir dados, experimentos, modelos treinados e monitoramento de desempenho ao longo do tempo.

MLOps trata especificamente dos desafios associados ao ciclo de vida de modelos de Machine Learning, incluindo rastreabilidade de experimentos, versionamento de datasets, reprodutibilidade de treinos, automação de pipelines, validação contínua, detecção de degradação de desempenho e retreinamento automatizado. A combinação dessas práticas permite que modelos deixem de ser protótipos isolados e passem a operar como serviços confiáveis em ambientes reais.

---

## O Papel da Containerização na Produção de Modelos

A containerização é uma técnica que permite empacotar uma aplicação junto com todas as suas dependências, bibliotecas e configurações em uma unidade isolada chamada container. Esse modelo garante que o software se comporte da mesma forma independentemente do ambiente em que for executado, seja em um computador local, em um servidor remoto ou em um cluster em nuvem.

No contexto de MLOps, containers são utilizados para encapsular pipelines de treino, serviços de inferência, APIs de modelos e jobs de processamento de dados. Essa abordagem facilita a escalabilidade, a automação de deploys, a replicação de ambientes e a integração com orquestradores como Kubernetes.

Docker é a tecnologia adotada neste capítulo como ferramenta principal para criação, execução e gerenciamento de containers, permitindo que os participantes criem imagens reprodutíveis e simulem cenários reais de produção.

---

## Estrutura do Conteúdo do Capítulo

Este capítulo contém exemplos práticos, imagens Docker, arquivos de configuração e scripts que demonstram como empacotar uma aplicação simples de Machine Learning em um container. Também são apresentados conceitos fundamentais sobre construção de imagens, execução de containers, gerenciamento de dependências e publicação de serviços de inferência.

O material foi projetado para funcionar como base para os capítulos seguintes, nos quais os containers serão integrados a pipelines, APIs, bancos vetoriais e arquiteturas distribuídas.

---

## Ambiente e Pré-requisitos

Para acompanhar as atividades deste capítulo, é esperado que o participante tenha conhecimentos básicos em Python e esteja familiarizado com o uso de terminal e Git. O ambiente recomendado inclui Python versão 3.9 ou superior e Docker instalado e configurado corretamente na máquina.

Caso o Docker não esteja instalado, recomenda-se seguir a documentação oficial para instalação conforme o sistema operacional utilizado.

---

## Quickstart: Executando o Capítulo Localmente

O primeiro passo consiste em clonar o repositório do workshop e acessar a pasta do capítulo CH1.

```bash
git clone https://github.com/seu-repo/workshop-nlp-mlops.git
cd workshop-nlp-mlops/mlops/CH1
```

Em seguida, recomenda-se criar um ambiente virtual Python para isolar dependências e instalar os pacotes necessários.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

Após a instalação das dependências, é possível executar localmente o exemplo base de aplicação de Machine Learning incluído neste capítulo.

```bash
python app/main.py
```

---

## Construindo a Imagem Docker

Este capítulo inclui um Dockerfile que empacota a aplicação em uma imagem de container pronta para produção. Para construir a imagem, utilize o comando abaixo.

```bash
docker build -t ch1-mlops-intro .
```

Após a construção, a imagem pode ser executada como um container local.

```bash
docker run -p 8000:8000 ch1-mlops-intro
```

Caso a aplicação exponha uma API, ela poderá ser acessada via navegador ou por ferramentas como curl ou Postman.

```bash
curl http://localhost:8000/health
```

---

## Objetivo Prático do Capítulo

Ao final deste capítulo, o participante deverá compreender como empacotar uma aplicação de Machine Learning de forma reprodutível, como isolar dependências utilizando containers e como simular um ambiente de produção local. Também será capaz de explicar o papel do Docker em pipelines de MLOps e como essa tecnologia se conecta com automação, integração contínua e deploy escalável.

O conhecimento adquirido neste módulo servirá como base para os próximos capítulos, nos quais serão integrados modelos de linguagem, bancos vetoriais, APIs de inferência, microsserviços e pipelines de CI/CD.

---

## Próximos Passos

Nos capítulos seguintes, os containers criados neste módulo serão estendidos para hospedar modelos de linguagem, integrar serviços de recuperação de informação, operar pipelines distribuídos e automatizar processos de entrega contínua em ambientes reais de produção.

