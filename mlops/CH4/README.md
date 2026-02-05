# CH4 — Infraestrutura Baseada em Servidores, Serverless e Autoscaling para Sistemas de IA

Este capítulo explora as principais estratégias de infraestrutura utilizadas para hospedar sistemas de Inteligência Artificial em produção, abordando desde arquiteturas tradicionais baseadas em máquinas virtuais até modelos modernos serverless e ambientes com autoscaling de containers.

O foco está na transição de serviços de IA funcionais para infraestruturas resilientes, escaláveis e economicamente eficientes, considerando cenários reais de uso em ambientes corporativos, acadêmicos e industriais. Ao longo deste módulo, o participante compreenderá como provisionar servidores, hospedar microsserviços, escalar aplicações automaticamente e selecionar arquiteturas adequadas conforme carga, custo e requisitos operacionais.

Os serviços construídos nos capítulos anteriores, como APIs de RAG, servidores de modelos de linguagem e bancos vetoriais, passam a ser implantados em ambientes de infraestrutura mais próximos dos utilizados em produção real.

---

## Arquiteturas Baseadas em Máquinas Virtuais e Servidores

Arquiteturas baseadas em máquinas virtuais continuam sendo amplamente utilizadas para hospedar aplicações críticas, especialmente quando há necessidade de controle total sobre o sistema operacional, recursos computacionais dedicados e configurações personalizadas.

Neste capítulo, o participante aprende a instanciar servidores virtuais para hospedar serviços de IA, configurar ambientes de execução, gerenciar dependências e expor aplicações para acesso externo. São discutidos aspectos relacionados a provisionamento, segurança básica, gerenciamento de processos, persistência de dados e boas práticas para manter serviços estáveis em execução contínua.

A execução de modelos de linguagem, APIs e pipelines de inferência em servidores dedicados é apresentada como uma abordagem robusta para workloads previsíveis ou de alta demanda.

---

## Serverless e Execução sob Demanda

O paradigma serverless permite executar aplicações sem a necessidade de gerenciar servidores explicitamente, delegando ao provedor de infraestrutura a responsabilidade por escalabilidade, disponibilidade e alocação de recursos.

Neste módulo, o participante compreende como serviços de IA podem ser adaptados para execução em ambientes serverless, explorando funções sob demanda, endpoints escaláveis automaticamente e arquiteturas orientadas a eventos. São discutidas vantagens como redução de custos operacionais, elasticidade automática e simplificação da manutenção, bem como limitações relacionadas a tempo de execução, latência inicial e restrições de recursos.

A adaptação de serviços de inferência e APIs de IA para modelos serverless demonstra como tornar aplicações mais flexíveis e economicamente viáveis para cargas variáveis.

---

## Autoscaling de Containers para Serviços de IA

À medida que a demanda por serviços de IA cresce, torna-se essencial implementar mecanismos de escalabilidade automática capazes de ajustar o número de instâncias em execução conforme o volume de requisições.

Neste capítulo, o participante aprende como configurar autoscaling para containers utilizando orquestradores e métricas de desempenho, permitindo que serviços de inferência se expandam ou reduzam dinamicamente. São explorados conceitos como escalabilidade horizontal, balanceamento de carga, monitoramento de uso de CPU e memória e estratégias para evitar gargalos ou degradação de desempenho.

Essa abordagem permite que sistemas de IA atendam desde poucos usuários até grandes volumes de tráfego sem necessidade de reconfiguração manual constante.

---

## Integração entre Infraestrutura e Microsserviços

Os microsserviços desenvolvidos no CH3 são integrados a ambientes de infraestrutura realistas, demonstrando como serviços distribuídos podem ser implantados em servidores, containers escaláveis e plataformas serverless.

Este capítulo enfatiza a importância de desacoplamento entre lógica de negócio e infraestrutura, permitindo que aplicações sejam movidas entre diferentes ambientes com mínima alteração de código. Também são discutidos aspectos relacionados a tolerância a falhas, replicação de serviços, recuperação automática e estratégias para manter alta disponibilidade.

---

## Estrutura do Capítulo

O conteúdo deste capítulo inclui arquivos de configuração para provisionamento de máquinas virtuais, exemplos de deploy de APIs em servidores, scripts para execução de serviços em containers escaláveis, configurações de autoscaling e exemplos de implantação em ambientes serverless.

Os artefatos produzidos aqui são projetados para serem reutilizados no próximo capítulo, onde serão integrados a pipelines automatizados de CI/CD e fluxos de entrega contínua.

---

## Ambiente e Pré-requisitos

Para acompanhar este capítulo, é esperado que o participante tenha concluído os módulos anteriores ou possua familiaridade com containers, APIs, microsserviços e serviços de IA. Também é necessário ter Docker instalado, além de acesso a um ambiente de nuvem ou máquina virtual para simular infraestrutura baseada em servidores.

Conhecimentos básicos sobre redes, HTTP e administração de sistemas são recomendados para melhor compreensão dos conceitos abordados.

---

## Quickstart: Acessando o Diretório do Capítulo

O primeiro passo consiste em navegar até a pasta correspondente ao CH4 dentro do repositório do workshop.

```bash
cd workshop-nlp-mlops/mlops/CH4
```

Caso seja necessário instalar dependências Python adicionais, recomenda-se configurar um ambiente virtual.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## Quickstart: Subindo os Serviços em um Servidor Local

Os serviços podem ser iniciados localmente para simular um ambiente baseado em servidores.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Após a inicialização, o serviço estará disponível para acesso externo conforme configuração de rede.

---

## Quickstart: Executando Serviços com Containers Escaláveis

Este capítulo inclui um arquivo docker-compose configurado para simular múltiplas instâncias de um serviço de inferência.

```bash
docker compose up --scale api=3
```

Esse comando inicia múltiplas réplicas do serviço, simulando escalabilidade horizontal.

---

## Quickstart: Simulando Autoscaling de Containers

Para testar políticas de escalabilidade automática, execute o script responsável por monitorar carga e ajustar instâncias.

```bash
python scripts/simulate_autoscaling.py
```

O script gera requisições artificiais e ajusta o número de containers ativos conforme a demanda simulada.

---

## Quickstart: Executando um Serviço em Modo Serverless

O capítulo inclui um exemplo de função serverless adaptada para inferência de IA, que pode ser executada localmente.

```bash
python serverless/run_function.py
```

Esse comando simula a execução sob demanda, acionando a função apenas quando uma requisição é recebida.

---

## Objetivo Prático do Capítulo

Ao final deste capítulo, o participante deverá ser capaz de implantar serviços de IA em ambientes baseados em servidores, configurar execução em plataformas serverless e implementar mecanismos de autoscaling para containers.

Também deverá compreender os trade-offs entre diferentes arquiteturas de infraestrutura, incluindo custo, desempenho, escalabilidade, latência e complexidade operacional. Esse conhecimento é fundamental para projetar sistemas de IA robustos, flexíveis e preparados para variações de carga em produção.

---

## Próximos Passos

No próximo capítulo, os serviços implantados neste módulo serão integrados a pipelines de CI/CD, permitindo automação completa do ciclo de vida de aplicações de IA, desde o versionamento de código até o deploy contínuo em ambientes de produção.

