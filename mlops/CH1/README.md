# CH1 - Fundamentos de MLOps e Docker

O objetivo deste material é apresentar o contexto histórico que levou ao surgimento do Docker, explicar como ele funciona internamente e demonstrar como utilizá-lo no dia a dia do desenvolvimento e da implantação de software.

## Contexto histórico e motivação

Antes do surgimento de containers, aplicações eram tradicionalmente executadas diretamente em servidores físicos ou virtuais. Em ambientes onde múltiplas aplicações coexistiam em um mesmo servidor, surgiam conflitos de dependências, incompatibilidades entre bibliotecas, divergências de versões de runtime e dificuldades na padronização dos ambientes de desenvolvimento, homologação e produção. Cada aplicação exigia configurações específicas, o que tornava o gerenciamento complexo e sujeito a falhas.

<img width="1040" height="588" alt="image" src="https://github.com/user-attachments/assets/abf0ae9e-7b72-412a-819c-623d6eb2cbcc" />

Para mitigar esses problemas, a virtualização ganhou força. Máquinas virtuais permitiram isolar aplicações em sistemas operacionais independentes, cada uma com seu próprio kernel, sistema de arquivos e conjunto de recursos. Embora eficaz em termos de isolamento, esse modelo apresentava custos elevados de consumo de memória, processamento e armazenamento, além de tempos de inicialização mais longos e maior sobrecarga operacional.

<img width="1046" height="591" alt="image" src="https://github.com/user-attachments/assets/15c2715c-0412-4431-bced-b586ddecaace" />

Com a evolução das tecnologias de kernel e isolamento de processos, surgiu o conceito moderno de containers. Diferente das máquinas virtuais, containers compartilham o kernel do sistema operacional hospedeiro, isolando apenas os processos, dependências e o sistema de arquivos necessários para a aplicação. Isso reduziu drasticamente o consumo de recursos e aumentou a eficiência na execução de workloads.

<img width="1044" height="587" alt="image" src="https://github.com/user-attachments/assets/45d48663-689d-49eb-8885-d1537229a9c4" />

O Docker emergiu como a plataforma que popularizou e padronizou o uso de containers, já que existem outras tecnologias que também trabalham com containers. Ele se consolidou como uma tecnologia open source amplamente adotada, com forte comunidade, integração com provedores de nuvem e um ecossistema robusto para distribuição e execução de aplicações em ambientes isolados .

## Conceito de containers e papel do Docker

Containers podem ser entendidos como unidades leves e portáteis que empacotam uma aplicação junto com todas as suas dependências, bibliotecas e configurações necessárias para execução. Ao compartilhar o kernel do sistema operacional, eles eliminam a necessidade de replicar recursos completos de um sistema operacional, como ocorre em máquinas virtuais, que precisam replicar interface gráfica, ferramentos de entrada e saída, todo o esquema de pastas e gerenciamento de processos próprios.

O Docker atua como uma plataforma para criar, distribuir e executar containers. Ele fornece ferramentas para empacotar aplicações em imagens, instanciar containers a partir dessas imagens e gerenciar o ciclo de vida dessas instâncias. Sua ampla adoção em ambientes de cloud, como Google Cloud Run e AWS Fargate, reforça seu papel como padrão de mercado para empacotamento e implantação de software moderno.

## Imagens Docker e containers

Um container Docker sempre é criado a partir de uma **imagem**. A imagem funciona como um modelo imutável que descreve tudo o que é necessário para executar uma aplicação, incluindo sistema de arquivos, dependências, variáveis de ambiente e comandos de inicialização. É importante compreender que uma imagem não é um container em execução; ela representa apenas a definição estática do ambiente. Podemos pensar nela como um instalador do ambiente no qual é possível rodar a aplicação que ela propõe.

As imagens podem ser listadas localmente utilizando o comando:

```bash
docker images
```

Elas podem ser obtidas a partir de repositórios públicos ou privados, como o [Docker Hub](https://hub.docker.com/), ou construídas localmente a partir de um arquivo de configuração chamado **Dockerfile**.

## Dockerfile e processo de build

O Dockerfile é um arquivo declarativo que descreve passo a passo como uma imagem deve ser construída. Podemos pensar nele como uma "receita" que diz como a imagem deve ser constrída. Ele define a imagem base, copia arquivos da aplicação, instala dependências, configura variáveis de ambiente e especifica o comando que será executado quando o container for iniciado .

Exemplo de Dockerfile:

```dockerfile
# Define uma imagem base para iniciar o build
FROM python:3.12.4 

# Define uma variável de ambiente
ENV PYTHONDONTWRITEBYTECODE=1

# Define uma pasta interna na imagem na qual vamos trabalhar a partir dessa linha
WORKDIR /app

# Copia o arquivo requirements.txt para dentro da pasta /app (onde estamos trabalhando) 
COPY requirements.txt . 

# Instala dependências do sistema
RUN pip install --no-cache-dir -r requirements.txt 

# Copia todo o restante dos arquivos da aplicação para a pasta /app
COPY . . 

# Define comando que será executado quando o container for iniciado
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
```

O processo de criação de uma imagem a partir de um Dockerfile é realizado com o comando:

```bash
docker build -f <DOCKERFILE> -t <CONTAINER_NAME> .
```

Esse comando instrui o Docker a ler o Dockerfile, executar cada instrução em sequência e gerar uma imagem final nomeada conforme especificado.

## Execução de containers

Após a criação da imagem, o próximo passo é instanciar um container em execução. Esse processo transforma a definição estática da imagem em um processo ativo no sistema operacional. O comando `docker run` permite iniciar containers com parâmetros específicos, como mapeamento de portas, volumes e modo interativo .

Um exemplo comum de execução é:

```bash
docker run -p <OUT_PORT>:<IN_PORT> -it <CONTAINER_NAME>
```

Esse comando associa uma porta externa da máquina hospedeira a uma porta interna do container, permitindo o acesso à aplicação a partir do ambiente externo.

Containers operam em um modelo de rede isolado, no qual cada instância possui sua própria interface virtual. O Docker permite expor serviços para fora do container por meio do mapeamento de portas, facilitando a comunicação entre aplicações e usuários externos. Esse mecanismo é essencial para executar servidores web, APIs e serviços distribuídos. Por esse motivo precisamos,muitas vezes, expor uma porta com a flag "-p" que mapeia qual porta externa <OUT_PORT> será linkada à porta interna do conteiner <IN_PORT>.

## Fluxo conceitual do Docker

O fluxo de trabalho no Docker segue uma sequência lógica que começa com a definição do Dockerfile, passa pela criação da imagem e culmina na execução do container. Esse modelo permite reprodutibilidade, portabilidade e padronização de ambientes, tornando o processo de desenvolvimento e implantação mais previsível e escalável .

<img width="1048" height="583" alt="image" src="https://github.com/user-attachments/assets/18ced274-c7a5-4535-96dd-a05aff681706" />

## Persistência de dados com volumes

Por padrão, os dados gerados dentro de um container são efêmeros e podem ser perdidos quando ele é removido. Para resolver esse problema, o Docker oferece o conceito de volumes, que permitem mapear diretórios do sistema hospedeiro para dentro do container. Dessa forma, arquivos e dados persistem independentemente do ciclo de vida da instância.

O comando típico para utilização de volumes é:

```bash
docker run -v <out_path>:<in_path> -it <CONTAINER_NAME>
```

Esse recurso é fundamental para bancos de dados, logs, arquivos de configuração e qualquer cenário que exija persistência.

Podemos pensar em um volume como uma pasta compartilhada entre o computador hospedeiro e o contaier. Alterações nessa pasta feitas no hospedeiro vão afetar a pasta interna do container e o contrário também ocorre. Por isso a existência da flag "-v" que define um uma pasta externa no sistema <out_path> que será linkada auma pasta interna do container <in_path>.

## Quickstart: Executando o Capítulo Localmente

O primeiro passo consiste em clonar o repositório do workshop e acessar a pasta do capítulo CH1.

```bash
git clone https://github.com/CEIA-UFG-GROUPS/ceia-ufg-workshop.git
cd workshop-nlp-mlops/mlops/CH1/practice
```

Em seguida, recomenda-se criar um ambiente virtual Python para isolar dependências e instalar os pacotes necessários.

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

Após a instalação das dependências, é possível executar localmente o exemplo base de aplicação de Machine Learning incluído neste capítulo.

```bash
python3 app/main.py
```

---

## Construindo a Imagem Docker

Este capítulo inclui um Dockerfile que empacota a aplicação em uma imagem de container pronta para produção. Para construir a imagem, utilize o comando abaixo.

```bash
docker build -t ch1-mlops-intro .
```

Após a construção, a imagem pode ser executada como um container local.

```bash
docker run -v ./logs/:/app/logs -p 8000:8000 ch1-mlops-intro # Linux
docker run -v "%cd%/logs:/app/logs" -p 8000:8000 ch1-mlops-intro # Windows CMD
```

Caso a aplicação exponha uma API, ela poderá ser acessada via navegador ou por ferramentas como curl ou Postman.

```bash
curl http://localhost:8000/
```

---

## Materiais

- [Slides](https://www.canva.com/design/DAHBZfHnu28/bXEE2GKGCRRtrJAmzLoLkA/edit?utm_content=DAHBZfHnu28&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
- [Documentação do Docker](https://docs.docker.com/guides/)
- [Developers Roadmap](https://github.com/kamranahmedse/developer-roadmap)
- [Docker Roadmap](https://roadmap.sh/docker)
- [História dos Containers](https://www.techtarget.com/searchitoperations/feature/Dive-into-the-decades-long-history-of-container-technology)
- [Análise de Desempenho entre Máquinas Virtuais e Containers](https://www.grupounibra.com/repositorio/REDES/2022/analise-de-desempenho-entre-maquinas-virtuais-e-containers-utilizando-o-docker3.pdf)
- [Containers e Virtualização](https://www.targetso.com/artigos/containers-e-virtualizacao/)
