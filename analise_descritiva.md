# Análise descritiva — Crescimento demográfico

## 1. Objetivo

Nesta parte do Projeto Integrador, analisei a mudança da população dos estados brasileiros entre 2010 e 2022. O objetivo é observar quais estados cresceram mais e como os valores variam entre eles.

## 2. Fonte e tratamento

Usei a Tabela 5 da publicação do Censo Demográfico 2022 do IBGE, com a população residente de cada UF em 2010 e 2022. Organizei os dados em um CSV com estado, região e os dois valores populacionais. O código verifica as colunas, converte as populações em números, remove linhas inválidas e calcula o crescimento acumulado.

**Fórmula utilizada:**

`crescimento (%) = ((população em 2022 / população em 2010) - 1) * 100`

A análise usa 27 unidades da federação. As taxas são calculadas para cada UF. A média das taxas estaduais é diferente da taxa de crescimento do Brasil como um todo.

## 3. Resultados na base completa

| Medida das taxas de crescimento por UF | Resultado |
|---|---:|
| Média | 8,98% |
| Mediana (Q2) | 7,06% |
| Q1 | 3,54% |
| Q3 | 11,06% |
| IQR | 7,53 pontos percentuais |
| Amplitude | 41,04 pontos percentuais |
| Desvio padrão populacional | 8,53 pontos percentuais |
| Variância populacional | 72,80 |
| Moda | Não existe moda única |

A média ficou maior que a mediana, o que sugere influência dos estados com as maiores taxas. A amplitude mostra que há diferenças grandes entre as UFs.

## 4. Outliers

Usei a regra de 1,5 vezes o IQR. Os limites calculados foram de **-7,76%** a **22,35%**. Roraima, com crescimento acumulado de **41,25%**, ultrapassou o limite superior e foi classificada como outlier. Isso não significa erro no IBGE, mas que seu crescimento ficou muito distante da maior parte dos estados.

## 5. Interpretação para gestores públicos

Roraima foi o estado com a maior taxa de crescimento no período, enquanto o Rio de Janeiro apresentou uma das menores taxas (aproximadamente 0,40%). Esse contraste pode ajudar gestores a investigar demandas diferentes de infraestrutura, transporte, saúde e educação.

É importante não tomar decisões apenas com a taxa percentual: um estado de população pequena pode crescer muito em porcentagem, mas aumentar menos em quantidade absoluta de habitantes do que um estado grande. Também seria necessário analisar dados municipais e faixas etárias para planejar serviços locais.

## 6. Limitações

Os dados usados aqui são de **dois Censos**, e não de todos os anos entre 2010 e 2022. Portanto, o painel compara o crescimento acumulado, não uma evolução ano a ano. Como a tabela escolhida só contém totais por UF, não há análise por faixa etária, sexo, raça ou município. Essas perguntas precisam de bases adicionais do IBGE.

## 7. Fonte

IBGE. Censo Demográfico 2022. **Tabela 5 — População residente e taxa média geométrica de crescimento anual — Brasil, Grandes Regiões e Unidades da Federação — 2010/2022**.

https://www.ibge.gov.br/biblioteca/visualizacao/livros/liv102011.pdf
