# Números que Falam — Crescimento Demográfico

**Parte individual 1 — crescimento demográfico das UFs (2010 a 2022).**

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

O dashboard carrega o CSV `dados/populacao_ibge_2010_2022.csv` e permite enviar outro CSV/XLSX que tenha as mesmas colunas. Possui filtros de região/UF, ano de referência, barras, boxplot e análise estatística. `analise.py` faz o tratamento e os cálculos.

**Fonte dos dados:** IBGE, Censo Demográfico 2022, tabela 5: https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv102011.pdf

**Limitação:** os dois pontos censitários não permitem mostrar anos intermediários, dados municipais ou faixas etárias. A média calculada é uma média simples das taxas de crescimento estaduais, não o crescimento ponderado nacional.

**Explicação para a apresentação:** o crescimento é calculado por `(população_2022 / população_2010 - 1) * 100`. Média e mediana resumem o comportamento dos estados. O IQR e o boxplot ajudam a identificar taxas de crescimento muito diferentes das demais.
