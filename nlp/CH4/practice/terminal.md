# Tutorial para rodar o projeto (CH4)

## 1) Pré-requisitos

- Python 3.10+
- Docker instalado e em execução
- Chave da OpenAI válida

## 2) Entrar na pasta do capítulo

```bash
cd nlp/CH4
```

## 3) Criar e ativar ambiente virtual

```bash
python -m venv venv
```

Ativar no Linux/macOS:

```bash
source venv/bin/activate
```

Ativar no Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

## 4) Instalar dependências

```bash
pip install -r requirements.txt
```

## 5) Subir o Qdrant

```bash
docker run -p 6333:6333 -d qdrant/qdrant
```

> A flag `-d` executa o container em segundo plano.

## 6) Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz de `nlp/CH4` com:

```env
OPENAI_API_KEY=sk-sua-chave-aqui
```

## 7) Executar scripts do projeto

### Ingestão no Qdrant

```bash
python src/ingestao.py
```

### Avaliação de métricas (100 primeiros IDs)

```bash
python src/metricas.py
```

### Teste de RAG via terminal

```bash
python src/rag.py
```

### Subir API

```bash
python src/api.py
```

## 8) Testar endpoint da API

Com a API rodando, em outro terminal execute:

```bash
curl -X POST "http://localhost:8000/rag" \
 -H "Content-Type: application/json" \
 -d '{"pergunta":"When did Beyonce start becoming popular?"}'
```
