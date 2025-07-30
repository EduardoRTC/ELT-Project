# Aprendendo Docker + Airflow
Ambiente de desenvolvimento local com Docker Compose

## Sobre
Projeto para aprender Docker e Apache Airflow configurando um ambiente completo usando containers.

### O que você vai aprender
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
git clone https://github.com/seu-usuario/docker-airflow.git
cd docker-airflow

# Crie as pastas
mkdir -p dags logs plugins