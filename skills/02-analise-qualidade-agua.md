# Skill 02 — Análise de Dados de Qualidade da Água

## Quando usar esta skill

Use esta skill para definir KPIs, perguntas analíticas, regras de interpretação e lógica de negócio do projeto **Azure Water Quality Data Lake**.

Domínio:

```text
Qualidade da água
ETA
ETE
Pontos de coleta
Parâmetros laboratoriais
Limites de referência
Conformidade e não conformidade
```

---

## KPIs oficiais do projeto

| KPI | Definição | Interpretação |
|---|---|---|
| Total de resultados | Quantidade total de análises registradas | Volume geral analisado |
| Total conformes | Resultados classificados como conformes | Indicador positivo |
| Total não conformes | Resultados fora do padrão | Indicador crítico |
| Total sem limite de referência | Resultados sem limite normativo configurado | Lacuna normativa/cadastral |
| Total com limite de referência | Resultados que possuem limite mínimo ou máximo | Base técnica para cálculo de conformidade |
| % conformidade geral | Conformes / total de resultados | Visão executiva geral |
| % conformidade com limite | Conformes / resultados com limite | Visão técnica mais justa |
| % não conformidade com limite | Não conformes / resultados com limite | Indicador de risco |

---

## Valores oficiais de validação

Todo dashboard, JSON ou consulta analítica deve bater estes números:

```text
Total de resultados: 72
Total conformes: 50
Total não conformes: 7
Total sem limite de referência: 15
Total com limite de referência: 57
% conformidade geral: 69,44%
% conformidade com limite: 87,72%
```

Fórmulas:

```text
% conformidade geral = 50 / 72 = 69,44%
% conformidade com limite = 50 / 57 = 87,72%
% não conformidade com limite = 7 / 57 = 12,28%
```

---

## Regra crítica de interpretação

Registros sem limite de referência não devem ser tratados como conformes nem como não conformes.

Eles devem aparecer como:

```text
Sem limite de referência
```

Motivo: não existe base normativa cadastrada para concluir se o valor está dentro ou fora do padrão.

---

## Perguntas analíticas principais

O dashboard deve responder rapidamente:

```text
1. Qual é o percentual geral de conformidade?
2. Qual é o percentual de conformidade considerando apenas resultados com limite?
3. Quantos resultados estão sem limite de referência?
4. Quais parâmetros mais apresentam não conformidade?
5. Quais pontos de coleta concentram maior número de não conformidades?
6. Quais tipos de ponto apresentam maior criticidade?
7. Como a conformidade evolui ao longo do tempo?
8. Quais parâmetros precisam de revisão de cadastro normativo?
9. Quais amostras concentram maior número de desvios?
10. A situação crítica está concentrada em ETA, ETE, rio ou reservatório?
```

---

## Segmentações importantes

Usar estas dimensões para análise:

```text
Parâmetro
Categoria do parâmetro
Ponto de coleta
Tipo de ponto
Município
Amostra
Responsável técnico
Status analítico
Competência de coleta
```

---

## Status analítico oficial

Usar exatamente estes três status:

```text
Conforme
Não conforme
Sem limite de referência
```

Lógica:

```text
Se possui_limite_referencia = 0 → Sem limite de referência
Se possui_limite_referencia = 1 e indicador_nao_conforme = 1 → Não conforme
Caso contrário → Conforme
```

---

## Rankings esperados

### Ranking de parâmetros críticos

Ordenar por:

```text
total_nao_conformes DESC
percentual_nao_conformidade_com_limite DESC
```

Mostrar pelo menos:

```text
parâmetro
categoria
unidade
quantidade de resultados
não conformes
sem limite
percentual de não conformidade
```

### Ranking de pontos críticos

Ordenar por:

```text
total_nao_conformes DESC
percentual_conformidade_com_limite ASC
```

Mostrar pelo menos:

```text
ponto de coleta
tipo de ponto
município
quantidade de resultados
conformes
não conformes
sem limite
percentual de conformidade
```

---

## Alertas analíticos sugeridos

| Condição | Alerta |
|---|---|
| Não conformidade > 0 | Existem parâmetros fora do padrão |
| Sem limite > 0 | Existem parâmetros sem referência normativa |
| % conformidade com limite < 90% | Atenção técnica recomendada |
| Ponto com 2 ou mais não conformidades | Ponto crítico prioritário |
| Parâmetro sem limite recorrente | Revisar cadastro normativo |

---

## Linguagem executiva para insights

Os insights devem ser objetivos, técnicos e acionáveis.

Exemplo de bom insight:

```text
O conjunto analisado apresenta 87,72% de conformidade entre resultados com limite de referência. As 7 não conformidades estão concentradas em parâmetros específicos, indicando necessidade de priorizar investigação por parâmetro e ponto de coleta.
```

Evitar:

```text
Os dados estão bons.
O dashboard está bonito.
Talvez precise analisar mais.
```

---

## Boas práticas de análise

- Separar visão executiva de visão técnica.
- Explicar sempre a diferença entre conformidade geral e conformidade com limite.
- Não mascarar registros sem limite.
- Priorizar ranking de criticidade por parâmetro e ponto.
- Usar percentuais com duas casas decimais.
- Usar contagens absolutas junto com percentuais.
- Evitar conclusões ambientais definitivas sem contexto normativo completo.
