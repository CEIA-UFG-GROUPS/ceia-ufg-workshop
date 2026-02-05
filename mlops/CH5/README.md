# CH5 — CI/CD, Cloud Build e Pipelines Automatizados para Sistemas de IA

Este capítulo consolida todo o conteúdo desenvolvido nos módulos anteriores ao introduzir práticas avançadas de Integração Contínua e Entrega Contínua aplicadas a sistemas de Inteligência Artificial. O foco está na automação completa do ciclo de vida de aplicações de IA, desde o versionamento de código e modelos até o build, testes, deploy e atualização contínua em ambientes de produção.

Ao longo deste módulo, o participante aprenderá como transformar projetos experimentais em pipelines automatizados, garantindo reprodutibilidade, confiabilidade, rastreabilidade e velocidade na entrega de soluções. São exploradas integrações com GitHub Actions e Cloud Build, além de estratégias modernas para automatizar testes, empacotamento de containers, validação de modelos e deploy contínuo de serviços de Machine Learning.

Este capítulo representa o fechamento do fluxo MLOps, conectando desenvolvimento, infraestrutura e operação em um pipeline contínuo e escalável.

---

## CI/CD Aplicado a Machine Learning e Inteligência Artificial

Pipelines tradicionais de CI/CD foram inicialmente projetados para software convencional, mas sistemas de Machine Learning exigem camadas adicionais de controle, como versionamento de dados, rastreamento de experimentos, validação de métricas de desempenho e governança de modelos.

Neste capítulo, CI/CD é tratado como um mecanismo para automatizar não apenas o deploy de código, mas também o treinamento, validação, empacotamento e publicação de modelos. O participante compreenderá como estruturar pipelines que executam testes automatizados, validam artefatos de Machine Learning, garantem consistência entre ambientes e reduzem o risco de regressões em produção.

A automação permite que novos modelos sejam promovidos para produção com segurança, baseados em critérios objetivos de desempenho e qualidade.

---

## GitHub Actions como Motor de Automação

GitHub Actions é utilizado como principal orquestrador de pipelines de integração e entrega contínua, permitindo que fluxos automatizados sejam acionados a cada commit, pull request ou tag de versão.

Neste módulo, o participante aprende a configurar workflows que executam validações de código, testes automatizados, builds de imagens Docker e deploy de serviços. Também são exploradas estratégias para versionamento semântico, controle de releases e segregação de ambientes entre desenvolvimento, homologação e produção.

Os workflows desenvolvidos automatizam a publicação de serviços de IA e pipelines MLOps, reduzindo a necessidade de intervenção manual e aumentando a confiabilidade operacional.

---

## Cloud Build e Pipelines de Build Distribuídos

Além da automação local e via GitHub Actions, o capítulo aborda o uso de serviços gerenciados de build, como Cloud Build, para executar pipelines de empacotamento e deploy em infraestrutura escalável.

O participante compreenderá como delegar o build de imagens Docker, a execução de testes e a publicação de artefatos para pipelines gerenciados, garantindo isolamento, escalabilidade e rastreabilidade das execuções.

Esse modelo permite que pipelines sejam executados em ambientes distribuídos, reduzindo dependência de máquinas locais e aumentando a robustez do processo de entrega.

---

## Versionamento de Código, Modelos e Artefatos

Sistemas de IA exigem controle rigoroso sobre versões de código, modelos treinados, datasets e configurações de execução. Neste capítulo, são abordadas estratégias para versionamento integrado, permitindo rastrear qual versão de um modelo está em produção, quais dados foram utilizados em seu treinamento e quais métricas justificaram sua promoção.

O participante aprenderá a estruturar pipelines que geram artefatos versionados, armazenam imagens Docker em registries, registram modelos treinados e mantêm histórico de releases, garantindo auditabilidade e governança.

---

## Deploy Contínuo de Serviços de IA

Os serviços desenvolvidos nos capítulos anteriores, incluindo APIs de RAG, microsserviços e pipelines de inferência, passam a ser implantados automaticamente sempre que uma nova versão válida é publicada.

Neste módulo, o participante aprenderá como configurar pipelines de deploy contínuo para ambientes baseados em servidores, containers ou plataformas serverless. São discutidas estratégias para evitar downtime, realizar rollback automático e validar saúde do sistema após cada atualização.

O deploy contínuo transforma a entrega de IA em um processo rápido, seguro e repetível, reduzindo drasticamente o tempo entre desenvolvimento e produção.

---

## Estrutura do Capítulo

Este capítulo inclui workflows do GitHub Actions, arquivos de configuração do Cloud Build, scripts de automação, templates de pipelines, exemplos de versionamento de modelos e integrações com registries de containers.

Os artefatos produzidos aqui representam um pipeline MLOps completo, integrando código, dados, modelos, infraestrutura e deploy automatizado.

---

## Ambiente e Pré-requisitos

Para acompanhar este capítulo, recomenda-se ter concluído os módulos anteriores e possuir familiaridade com Git, Docker, APIs, microsserviços e infraestrutura de nuvem.

Também é necessário ter uma conta no GitHub para execução dos workflows e acesso a um registry de containers, além de permissões para executar builds e deploys em ambiente de nuvem ou infraestrutura local simulada.

---

## Quickstart: Acessando o Diretório do Capítulo

O primeiro passo consiste em navegar até a pasta correspondente ao CH5 dentro do repositório do workshop.

```bash
cd workshop-nlp-mlops/mlops/CH5
```

Caso seja necessário instalar dependências adicionais, recomenda-se ativar um ambiente virtual Python.

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## Quickstart: Executando um Pipeline Local de Build

Este capítulo inclui um script para simular localmente a execução de um pipeline de build e validação.

```bash
bash scripts/run_local_pipeline.sh
```

Esse comando executa testes, valida o código, constrói a imagem Docker e prepara os artefatos para deploy.

---

## Quickstart: Configurando GitHub Actions

Para ativar o pipeline automatizado no GitHub, é necessário copiar o workflow para a pasta correta do repositório.

```bash
mkdir -p .github/workflows
cp workflows/mlops-ci-cd.yml .github/workflows/
git add .github/workflows/mlops-ci-cd.yml
git commit -m "Add CI/CD pipeline"
git push origin main
```

Após o push, o workflow será executado automaticamente a cada atualização no repositório.

---

## Quickstart: Build e Push de Imagem Docker Automatizado

O pipeline inclui uma etapa de build e publicação de imagem Docker em um registry.

```bash
docker build -t your-user/ch5-mlops:latest .
docker push your-user/ch5-mlops:latest
```

Esse processo também pode ser automatizado dentro do pipeline de CI/CD.

---

## Quickstart: Executando Deploy Automatizado

Uma vez que a imagem esteja publicada, o deploy do serviço pode ser executado automaticamente ou manualmente para fins de teste.

```bash
bash scripts/deploy_service.sh
```

O script publica a nova versão do serviço em ambiente configurado, validando sua disponibilidade após o deploy.

---

## Quickstart: Simulando Atualização Contínua de Modelo

O capítulo inclui um exemplo de pipeline que detecta mudanças em um modelo e dispara uma atualização automática em produção.

```bash
python pipelines/simulate_model_update.py
```

Esse comando simula o retreinamento, validação e promoção de um novo modelo, demonstrando um fluxo completo de MLOps.

---

## Objetivo Prático do Capítulo

Ao final deste capítulo, o participante deverá ser capaz de estruturar pipelines completos de CI/CD para sistemas de IA, automatizar build e deploy de serviços, versionar modelos e artefatos e operar fluxos de entrega contínua em ambientes de produção.

Também deverá compreender como integrar engenharia de software, Machine Learning e infraestrutura em um pipeline unificado, reduzindo riscos operacionais e acelerando a entrega de soluções inteligentes.

Esse conhecimento representa o estágio final da maturidade MLOps apresentada neste workshop, aproximando o participante de práticas utilizadas em times profissionais de engenharia de IA.

---

## Encerramento do Módulo MLOps

Com a conclusão deste capítulo, o participante terá percorrido todo o ciclo de vida de um sistema moderno de Inteligência Artificial em produção, desde a containerização inicial até a automação completa de deploy e atualização contínua.

O conteúdo deste módulo fornece uma base sólida para atuação em times de NLP, MLOps, DevOps e Engenharia de IA, além de servir como referência prática para projetos reais em ambientes corporativos e de pesquisa.

