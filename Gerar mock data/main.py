import pandas as pd
import numpy as np
import random
from faker import Faker
from pathlib import Path

fake = Faker("pt_BR")
random.seed(2025)
np.random.seed(2025)

# --- Configurações ---
N_LINHAS = 1_000

# Mapeamento fixo de vendedores → nome → cidade/estado
vendedores = {
    1: {"nome": "João Silva",     "cidade": "São Paulo",       "estado": "SP"},
    2: {"nome": "Maria Souza",    "cidade": "Rio de Janeiro",  "estado": "RJ"},
    3: {"nome": "Carlos Pereira", "cidade": "Curitiba",        "estado": "PR"},
    4: {"nome": "Ana Oliveira",   "cidade": "Salvador",        "estado": "BA"},
    5: {"nome": "Fernando Costa", "cidade": "Belo Horizonte",  "estado": "MG"},
}

# 10 produtos fixos: id → nome, categoria, preço unitário fixo
produtos = {
    101: {"nome": "Notebook X1",        "categoria": "Eletrônicos",      "preco_unit": 3500.00},
    102: {"nome": "Cafeteira 20L",      "categoria": "Eletrodomésticos", "preco_unit": 600.00},
    103: {"nome": "Tênis Corrida",      "categoria": "Calçados",         "preco_unit": 350.00},
    104: {"nome": "Camisa Polo",        "categoria": "Vestuário",        "preco_unit": 120.00},
    105: {"nome": "Smartphone A9",      "categoria": "Eletrônicos",      "preco_unit": 2800.00},
    106: {"nome": "Headset Gamer H1",   "categoria": "Eletrônicos",      "preco_unit": 450.00},
    107: {"nome": "Jaqueta Esportiva",  "categoria": "Vestuário",        "preco_unit": 250.00},
    108: {"nome": "Tablet T10",         "categoria": "Eletrônicos",      "preco_unit": 1500.00},
    109: {"nome": "Liquidificador X",   "categoria": "Eletrodomésticos", "preco_unit": 300.00},
    110: {"nome": "Fone Bluetooth B1",  "categoria": "Eletrônicos",      "preco_unit": 200.00},
}

canais = ["loja_fisica", "ecommerce"]

# ---------- Utilitários ----------
def gerar_desconto(canal: str):
    """Retorna desconto aleatório ou NaN (10 % de blanks)."""
    if random.random() < 0.10:
        return np.nan
    max_desc = 0.15 if canal == "ecommerce" else 0.30
    return round(random.uniform(0, max_desc), 2)

def gerar_qtd():
    """Quantidade entre 1 e 10 (1 % de blanks)."""
    return np.nan if random.random() < 0.01 else random.randint(1, 10)

def gerar_comentario():
    """Comentário opcional (30 % de presença)."""
    return fake.sentence(nb_words=random.randint(10, 20)) if random.random() < 0.30 else np.nan

# ---------- Geração dos registros ----------
registros = []
for venda_id in range(1, N_LINHAS + 1):
    data_venda = fake.date_between(start_date="-1y", end_date="today").strftime("%d-%m-%Y")
    canal = random.choices(canais, weights=[0.7, 0.3])[0]  # 70 % loja física

    # Produto fixo
    produto_id = random.choice(list(produtos.keys()))
    prod = produtos[produto_id]

    # Vendedor & localização
    if canal == "loja_fisica":
        vendedor_id = random.choice(list(vendedores.keys()))
        v_info = vendedores[vendedor_id]
        vendedor_nome = v_info["nome"]
        cidade = v_info["cidade"]
        estado = v_info["estado"]
        # 5 % de blanks em nome e 5 % em id
        if random.random() < 0.05:
            vendedor_nome = np.nan
        if random.random() < 0.05:
            vendedor_id = np.nan
    else:  # ecommerce => sem vendedor
        vendedor_id = np.nan
        vendedor_nome = np.nan
        # cidade/estado — 5 % blanks
        if random.random() < 0.05:
            cidade = np.nan
            estado = np.nan
        else:
            cidade = fake.city()
            estado = fake.estado_sigla()

    preco_unit = prod["preco_unit"]
    # 2 % blanks em preço
    if random.random() < 0.02:
        preco_unit = np.nan

    qtd = gerar_qtd()
    desconto = gerar_desconto(canal)
    comentarios = gerar_comentario()

    registros.append([
        venda_id, data_venda, vendedor_id, vendedor_nome,
        produto_id, prod["nome"], prod["categoria"],
        preco_unit, qtd, desconto, canal, cidade, estado, comentarios
    ])

# ---------- DataFrame ----------
colunas = [
    "venda_id", "data", "vendedor_id", "vendedor_nome", "produto_id", "produto_nome",
    "categoria", "preco_unit", "qtd", "desconto", "canal", "cidade", "estado", "comentarios"
]
df = pd.DataFrame(registros, columns=colunas)

# ---------- Salvar no mesmo diretório do script ----------
script_dir = Path(__file__).resolve().parent
arquivo_saida = script_dir / "vendas_mock.csv"

df.to_csv(arquivo_saida, index=False, encoding="utf-8")
print(f"Arquivo salvo em: {arquivo_saida}")
