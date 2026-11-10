"""Funções de limpeza e estatística para o indicador de crescimento populacional."""

import pandas as pd
import numpy as np

COLUNAS = ["uf", "regiao", "populacao_2010", "populacao_2022"]


def tratar_dados(tabela):
    dados = tabela.copy()
    dados.columns = dados.columns.str.strip().str.lower()
    faltando = [col for col in COLUNAS if col not in dados.columns]
    if faltando:
        raise ValueError("Colunas que faltam no arquivo: " + ", ".join(faltando))

    dados = dados[COLUNAS].copy()
    dados["uf"] = dados["uf"].astype("string").str.strip()
    dados["regiao"] = dados["regiao"].astype("string").str.strip()
    for coluna in ["populacao_2010", "populacao_2022"]:
        dados[coluna] = pd.to_numeric(dados[coluna], errors="coerce")

    dados = dados.dropna(subset=COLUNAS)
    dados = dados[(dados["populacao_2010"] > 0) & (dados["populacao_2022"] > 0)]
    dados = dados.drop_duplicates(subset="uf", keep="first")
    dados["crescimento_percentual"] = (
        (dados["populacao_2022"] / dados["populacao_2010"] - 1) * 100
    )
    dados["diferenca_habitantes"] = dados["populacao_2022"] - dados["populacao_2010"]
    return dados.reset_index(drop=True)


def calcular_estatisticas(valores):
    serie = pd.to_numeric(pd.Series(valores), errors="coerce").dropna()
    if serie.empty:
        raise ValueError("Não há valores válidos para calcular as estatísticas.")

    q1, mediana, q3 = np.percentile(serie, [25, 50, 75])
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    modas = serie.mode()
    # Se cada taxa for diferente, não existe moda única.
    moda = float(modas.iloc[0]) if len(modas) < len(serie) else None

    return {
        "quantidade": len(serie),
        "media": float(serie.mean()),
        "mediana": float(mediana),
        "moda": moda,
        "q1": float(q1),
        "q2": float(mediana),
        "q3": float(q3),
        "iqr": float(iqr),
        "amplitude": float(serie.max() - serie.min()),
        "variancia": float(serie.var(ddof=0)),
        "desvio_padrao": float(serie.std(ddof=0)),
        "limite_inferior": float(limite_inferior),
        "limite_superior": float(limite_superior),
    }


def identificar_outliers(dados, coluna="crescimento_percentual"):
    resumo = calcular_estatisticas(dados[coluna])
    return dados[
        (dados[coluna] < resumo["limite_inferior"])
        | (dados[coluna] > resumo["limite_superior"])
    ].copy()
