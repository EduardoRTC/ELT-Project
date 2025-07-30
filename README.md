# Aprendendo Docker + Airflow + DATABRICKS
Ambiente de desenvolvimento local com Docker Compose

## Sobre
Projeto para aprender Docker e Apache Airflow configurando um ambiente completo usando containers.

### Quais ferramentas utilizar ?
* **Docker**: Containerização, imagens, volumes, networks
* **Docker Compose**: Orquestração multi-container, variáveis de ambiente
* **Apache Airflow**: Interface web, DAGs, tasks, scheduling
* **Dev Containers**: Desenvolvimento dentro de containers com VS Code
* **Estrutura de projeto**: Organização de código, logs, plugins
* **Troubleshooting**: Logs, debugging, reinicialização de serviços

## Pré-requisitos
* Docker 20.10+
* Docker Compose v2
* VS Code + extensão Dev Containers
* 4GB RAM livre

---

## Como usar

### 1. Clone e configure
```bash
git clone https://github.com/EduardoRTC/docker-airflow-databricks-practice
cd docker-airflow
```

### 2. Subir os containers
```bash
docker compose up -d
```

### 3. Aguarde todos os serviços subirem
```bash
# Verifique o status dos containers
docker compose ps

# Acompanhe os logs (opcional)
docker compose logs -f
```

⏳ **Aguarde 2-3 minutos** para que todos os serviços estejam completamente prontos.

### 4. Acesse o Airflow
* **URL**: http://localhost:8080
* **Usuário**: `airflow`
* **Senha**: `airflow`

### 5. Dev Container (Opcional)
Para desenvolver diretamente dentro do container:
* Abra o projeto no VS Code
* `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
* Aguarde o ambiente carregar
* Desenvolva com acesso completo ao ambiente Airflow

---

## Configurações Incluídas

### Conexão Databricks
O Docker Compose está customizado para criar automaticamente uma conexão Databricks:
* **Connection ID**: `databricks_default`
* **Connection Type**: `databricks`
* Configure suas credenciais nas variáveis de ambiente (.env)

```bash
# Adicione no arquivo .env
DATABRICKS_HOST=https://seu-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi123...
```

---

## Estrutura
```
docker-airflow/
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
├── .devcontainer/
│   └── devcontainer.json
├── dags/
├── logs/
└── plugins/
```

## Comandos úteis
```bash
# Ver status
docker compose ps

# Parar
docker compose down

# Logs específicos
docker compose logs airflow-webserver
docker compose logs airflow-scheduler

# Acessar container
docker compose exec airflow-webserver bash

# Reiniciar serviço específico
docker compose restart airflow-webserver
```

---

## Stack
* Apache Airflow 2.8+
* PostgreSQL 13
* Redis 7
* Docker + Compose
* VS Code Dev Containers
* Databricks Provider