# ELT – Análises de performance e detecção de anomalias.
Arquitetura Medallion • Airflow 3 • PySpark 4 • Databricks

## 1. Visão Geral 🚀
Pipeline ELT em quatro camadas (Landing → Bronze → Silver → Gold) que:

* recebe arquivo `rel_vendas.xlsx`;
* limpa e enriquece os dados segundo regras de negócio;
* gera um **dataset Gold** pronto para análise de performance e detecção de anomalias.

### Tecnologias
* Apache **Airflow 3.0.3** (Python 3.12) – orquestração  
* **PySpark 4.0.0** – transformações distribuídas  
* **Databricks** provider 7.6.0 – execução em cluster / DBFS  
* **PostgreSQL 13** – metadados do Airflow  
* Docker + Compose – empacotamento local

---

## 2. Estrutura do Arquivo de Origem
Arquivo entregue: `rel_vendas.csv`  

Principais campos (landing):

* `venda_id` – id único da venda  
* `data` – data da venda  
* `vendedor_id`, `vendedor_nome`  
* `produto_id`, `produto_nome`, `categoria`  
* `preco_unit`, `qtd`, `desconto`  
* `canal` – loja_fisica, ecommerce, app  
* `cidade`, `estado`, `comentarios`

---

## 3. Regras por Camada

### 3.1 Landing (Raw Zone)
* Apenas salva o arquivo original em `/landing/yyyy/MM/dd/`.  
* Registra nome e data de recebimento.

### 3.2 Bronze (Clean Zone)
* Remove linhas com nulos críticos (`venda_id`, `data`, `produto_id`, `vendedor_id`, `preco_unit`, `qtd`).  
* Converte tipos (`data` → date, `preco_unit` → float, `qtd` → int).  
* Padroniza nomes de colunas (snake_case).  

### 3.3 Silver (Trusted Zone)
* **`valor_total`** = `preco_unit * qtd * (1 - desconto)`.  
* **`score_venda`**  
  * ALTO_RISCO → desconto > 20 %  
  * VENDA_PREMIUM → valor_total > R$ 1 000  
  * NORMAL → demais casos  
* **`flag_anomalia`** – TRUE se `preco_unit` estiver ±30 % fora da média da categoria.  
* Remove colunas de texto livre e endereço (`vendedor_nome`, `produto_nome`, `comentarios`, `cidade`, `estado`).  
* Mantém apenas: ids, data, categoria, preço, quantidade, desconto, canal, valor_total, score_venda, flag_anomalia.

### 3.4 Gold (Final Zone)
* Exporta `vendas_gold_YYYYMMDD.csv` para `/gold/yyyy/MM/dd/`.  
* Campos finais: `venda_id`, `data`, `vendedor_id`, `produto_id`, `categoria`, `valor_total`, `desconto`, `score_venda`, `flag_anomalia`.

---

## 4. Controle de Execução
A cada execução o Airflow grava:

* nome do arquivo e timestamp  
* camada processada  
* linhas recebidas / válidas  
* colunas removidas / mantidas  
* regras aplicadas  
* hash SHA‑256 (opcional)  
* status (sucesso / erro)

---

## 5. Rodando Localmente 🏃‍♂️

### Pré‑requisitos
* Docker 20.10+ e Docker Compose v2  
* Workspace e token Databricks

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/<user>/elt-vendas.git
cd elt-vendas

# 2. Crie pastas locais
mkdir -p dags logs plugins

# 3. Exporte variáveis do Databricks
export DATABRICKS_HOST="https://<workspace>.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi<token>"

# 4. Suba tudo
docker compose up --build

O terminal exibirá algo como:
Simple auth manager | Password for user 'admin': AbC123xYz