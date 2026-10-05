"""Análise alternativa das transações da ClearBank usando pandas.

Implementa a mesma lógica de limpeza e agrupamento mensal do notebook
principal (desafio-final.ipynb), mas usando pandas em vez do módulo csv
nativo. Serve para comparar os resultados das duas abordagens (requisito
opcional RO1 do desafio).

Uso:
    python analise_pandas.py
"""

import pandas as pd

ARQUIVO_CSV = "transacoes.csv"
LIMITE_SUSPEITO = 10000.00


def carregar_dados(caminho=ARQUIVO_CSV):
    """Lê o CSV com pandas, mantendo todas as colunas como texto por enquanto."""
    return pd.read_csv(caminho, dtype=str)


def limpar_dados(df):
    """Aplica as mesmas regras de validação do notebook principal e retorna
    (dataframe apenas com as linhas válidas, total de linhas lidas, total de inválidas)."""
    df = df.copy()

    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    df["cliente_id"] = df["cliente_id"].fillna("").str.strip()
    df["tipo"] = df["tipo"].fillna("").str.strip().str.lower()

    total_lidas = len(df)

    mascara_valida = (
        df["id"].notna()
        & (df["cliente_id"] != "")
        & df["data"].notna()
        & df["tipo"].isin(["credito", "debito"])
        & df["valor"].notna()
        & (df["valor"] > 0)
    )

    df_validas = df[mascara_valida].copy()
    df_validas["mes"] = df_validas["data"].dt.strftime("%Y-%m")

    total_invalidas = total_lidas - len(df_validas)
    return df_validas, total_lidas, total_invalidas


def agrupar_por_mes(df_validas):
    """Agrupa as transações válidas por mês e calcula as mesmas métricas
    da solução nativa: quantidade, total crédito/débito, saldo, média,
    maior e menor valor."""
    resumo = df_validas.groupby("mes").agg(
        quantidade=("valor", "count"),
        media=("valor", "mean"),
        maior_valor=("valor", "max"),
        menor_valor=("valor", "min"),
    )

    total_credito = df_validas[df_validas["tipo"] == "credito"].groupby("mes")["valor"].sum()
    total_debito = df_validas[df_validas["tipo"] == "debito"].groupby("mes")["valor"].sum()

    resumo["total_credito"] = total_credito
    resumo["total_debito"] = total_debito
    resumo[["total_credito", "total_debito"]] = resumo[["total_credito", "total_debito"]].fillna(0.0)
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]

    return resumo


def identificar_suspeitas(df_validas, limite=LIMITE_SUSPEITO):
    """Retorna as linhas com valor acima do limite de suspeita."""
    return df_validas[df_validas["valor"] > limite]


def main():
    df = carregar_dados()
    df_validas, total_lidas, total_invalidas = limpar_dados(df)

    print(f"Total de linhas lidas: {total_lidas}")
    print(f"Linhas válidas: {len(df_validas)}")
    print(f"Linhas inválidas: {total_invalidas}")
    print()

    resumo = agrupar_por_mes(df_validas)
    colunas = ["quantidade", "total_credito", "total_debito", "saldo", "media", "maior_valor", "menor_valor"]
    print(resumo[colunas])
    print()

    suspeitas = identificar_suspeitas(df_validas)
    print("===== TRANSAÇÕES SUSPEITAS =====")
    if suspeitas.empty:
        print("Nenhuma transação suspeita encontrada.")
    else:
        for _, linha in suspeitas.iterrows():
            data_formatada = linha["data"].strftime("%Y-%m-%d")
            print(f"ID: {int(linha['id'])} | Cliente: {linha['cliente_id']} | "
                  f"Data: {data_formatada} | Valor: R$ {linha['valor']:.2f}")


if __name__ == "__main__":
    main()
