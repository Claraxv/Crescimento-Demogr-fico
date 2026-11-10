"""Dashboard individual - Projeto Integrador Python e Matemática."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from analise import calcular_estatisticas, identificar_outliers, tratar_dados

st.set_page_config(page_title="Números que Falam", page_icon="📊", layout="wide")
st.title("📊 Números que Falam")
st.subheader("Crescimento demográfico no Brasil — 2010 a 2022")
st.write("Projeto Integrador de Python e Matemática | Parte individual")

st.sidebar.header("Filtros e dados")
arquivo = st.sidebar.file_uploader("Enviar outra base do IBGE", type=["csv", "xlsx"])

try:
    if arquivo is None:
        caminho = Path(__file__).parent / "dados" / "populacao_ibge_2010_2022.csv"
        tabela = pd.read_csv(caminho)
        st.sidebar.caption("Base padrão: Censos IBGE 2010 e 2022")
    elif arquivo.name.lower().endswith(".csv"):
        try:
            tabela = pd.read_csv(arquivo, sep=None, engine="python")
        except UnicodeDecodeError:
            arquivo.seek(0)
            tabela = pd.read_csv(arquivo, sep=None, engine="python", encoding="latin-1")
    else:
        tabela = pd.read_excel(arquivo)
    dados = tratar_dados(tabela)
except (ValueError, OSError, pd.errors.ParserError) as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.info("O arquivo precisa conter: uf, regiao, populacao_2010, populacao_2022")
    st.stop()

if dados.empty:
    st.warning("A base ficou sem registros válidos após a limpeza.")
    st.stop()

regioes = st.sidebar.multiselect(
    "Regiões", sorted(dados["regiao"].unique().tolist()),
    default=sorted(dados["regiao"].unique().tolist())
)
por_regiao = dados[dados["regiao"].isin(regioes)]
estados_disponiveis = sorted(por_regiao["uf"].tolist())
estados = st.sidebar.multiselect("Estados (UF)", estados_disponiveis, default=estados_disponiveis)
ano = st.sidebar.selectbox("Ano para comparar a população", [2010, 2022], index=1)
filtrados = por_regiao[por_regiao["uf"].isin(estados)].copy()

if filtrados.empty:
    st.warning("Selecione pelo menos um estado para ver os resultados.")
    st.stop()

st.markdown("### Resumo do crescimento por estado")
st.caption("As medidas abaixo descrevem a distribuição das taxas de crescimento dos estados selecionados, e não a taxa nacional.")
estatisticas = calcular_estatisticas(filtrados["crescimento_percentual"])
outliers = identificar_outliers(filtrados)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Média das taxas", f"{estatisticas['media']:.2f}%")
c2.metric("Mediana", f"{estatisticas['mediana']:.2f}%")
c3.metric("IQR", f"{estatisticas['iqr']:.2f} p.p.")
c4.metric("Outliers", len(outliers))

c5, c6, c7 = st.columns(3)
c5.metric("Desvio padrão", f"{estatisticas['desvio_padrao']:.2f} p.p.")
c6.metric("Amplitude", f"{estatisticas['amplitude']:.2f} p.p.")
c7.metric("População selecionada em " + str(ano), f"{int(filtrados[f'populacao_{ano}'].sum()):,}".replace(",", "."))

st.markdown("### Gráficos")
aba1, aba2, aba3 = st.tabs(["Crescimento (%)", "Boxplot", "População por ano"])
with aba1:
    grafico = px.bar(
        filtrados.sort_values("crescimento_percentual"), x="uf", y="crescimento_percentual",
        color="regiao", title="Crescimento acumulado entre 2010 e 2022",
        labels={"uf": "Estado", "crescimento_percentual": "Crescimento (%)", "regiao": "Região"}
    )
    st.plotly_chart(grafico, use_container_width=True)
with aba2:
    grafico = px.box(filtrados, y="crescimento_percentual", points="all", hover_name="uf",
                     title="Distribuição das taxas por estado",
                     labels={"crescimento_percentual": "Crescimento (%)"})
    st.plotly_chart(grafico, use_container_width=True)
with aba3:
    grafico = px.bar(
        filtrados.sort_values(f"populacao_{ano}", ascending=False), x="uf", y=f"populacao_{ano}",
        color="regiao", title=f"População por estado no Censo {ano}",
        labels={"uf": "Estado", f"populacao_{ano}": "Habitantes", "regiao": "Região"}
    )
    st.plotly_chart(grafico, use_container_width=True)

st.markdown("### Outras medidas estatísticas")
st.write(f"Q1: **{estatisticas['q1']:.2f}%** | Q2: **{estatisticas['q2']:.2f}%** | Q3: **{estatisticas['q3']:.2f}%**")
moda_texto = "não há moda única" if estatisticas["moda"] is None else f"{estatisticas['moda']:.2f}%"
st.write(f"Variância: **{estatisticas['variancia']:.2f}** | Moda: **{moda_texto}**")
st.write(f"Limites para outliers (1,5 × IQR): **{estatisticas['limite_inferior']:.2f}%** até **{estatisticas['limite_superior']:.2f}%**")
if outliers.empty:
    st.info("Nenhum estado foi classificado como outlier nesse filtro.")
else:
    st.write("**Estados considerados outliers:**")
    st.dataframe(outliers[["uf", "crescimento_percentual"]], hide_index=True)

st.markdown("### Interpretação dos resultados")
maior = filtrados.loc[filtrados["crescimento_percentual"].idxmax()]
menor = filtrados.loc[filtrados["crescimento_percentual"].idxmin()]
st.write(
    f"Entre os estados selecionados, {maior['uf']} teve o maior crescimento acumulado "
    f"({maior['crescimento_percentual']:.2f}%) e {menor['uf']} teve o menor "
    f"({menor['crescimento_percentual']:.2f}%)."
)
if estatisticas["media"] > estatisticas["mediana"]:
    st.write("A média é maior que a mediana. Isso pode indicar que estados com crescimento mais alto estão puxando a média para cima.")
elif estatisticas["media"] < estatisticas["mediana"]:
    st.write("A média é menor que a mediana. Alguns crescimentos mais baixos podem influenciar o resultado geral.")
else:
    st.write("A média e a mediana são iguais nesse recorte.")
st.write("Esses dados podem ajudar gestores públicos a comparar o ritmo de crescimento dos estados e planejar serviços e infraestrutura.")
st.caption("Atenção: comparar apenas dois Censos não permite analisar a trajetória ano a ano nem a distribuição por idade ou município.")

st.markdown("### Dados usados")
st.dataframe(filtrados, hide_index=True, use_container_width=True)
st.download_button("Baixar CSV tratado", dados.to_csv(index=False).encode("utf-8-sig"),
                   file_name="populacao_tratada.csv", mime="text/csv")

st.markdown("### Fonte e contexto")
st.write("Fonte: IBGE, Censos Demográficos 2010 e 2022, Tabela 5 (população de 2010 compatibilizada com o território de 2022).")
st.markdown("[Consultar publicação do IBGE](https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv102011.pdf)")
st.markdown("[Conhecer o Censo Demográfico](https://censo2022.ibge.gov.br/)")
st.write("**Pergunta para os gestores:** quais estados merecem atenção especial no planejamento de infraestrutura diante do crescimento populacional?")
