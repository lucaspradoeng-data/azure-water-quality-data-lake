# Skill 04 — Visualização HTML do Azure Water Quality Data Lake

## Quando usar esta skill

Use esta skill para criar ou ajustar o dashboard HTML do projeto **Azure Water Quality Data Lake**.

O dashboard deve ser uma entrega rápida, apresentável e versionável, consumindo JSONs exportados do Azure SQL.

Fluxo oficial:

```text
Azure SQL Views
  ↓
data/dashboard/*.json
  ↓
dashboard/index.html
  ↓
dashboard/css/style.css
  ↓
dashboard/js/app.js
```

---

## Objetivo do dashboard

Criar uma página única, visualmente profissional, para apresentar rapidamente os principais indicadores de qualidade da água.

O dashboard deve responder:

```text
1. Qual é a conformidade geral?
2. Qual é a conformidade técnica considerando apenas resultados com limite?
3. Quantos resultados estão não conformes?
4. Quantos resultados estão sem limite de referência?
5. Quais parâmetros são mais críticos?
6. Quais pontos de coleta são mais críticos?
7. Como a conformidade evolui no tempo?
```

---

## Fontes de dados JSON

Consumir os arquivos locais:

```text
data/dashboard/kpi_conformidade_geral.json
data/dashboard/conformidade_por_parametro.json
data/dashboard/conformidade_por_ponto_coleta.json
data/dashboard/evolucao_mensal_conformidade.json
data/dashboard/analise_conformidade.json
```

Regra crítica:

```text
Não conectar o HTML diretamente no Azure SQL.
Não colocar credenciais no HTML, CSS ou JS.
```

---

## Estrutura obrigatória

```text
dashboard
├── index.html
├── css
│   └── style.css
└── js
    └── app.js
```

---

## Layout recomendado

Página única com:

```text
1. Header do projeto
2. Status da base e data de geração
3. Cards de KPIs principais
4. Gráfico de distribuição por status analítico
5. Ranking de parâmetros críticos
6. Ranking de pontos de coleta críticos
7. Evolução mensal de conformidade
8. Tabela resumida de resultados
9. Área de insights gerados por IA ou insights automáticos locais
```

---

## KPIs obrigatórios

Mostrar cards para:

```text
Total de resultados: 72
Conformes: 50
Não conformes: 7
Sem limite de referência: 15
% conformidade geral: 69,44%
% conformidade com limite: 87,72%
```

---

## Design system recomendado

Tema: dark técnico/profissional, com opção de light mode se possível.

Estilo:

```text
visual moderno
cards executivos
gráficos limpos
boa leitura
sem poluição visual
prioridade para clareza analítica
```

Paleta sugerida:

```css
:root {
  --bg: #07111f;
  --bg2: #0b1b2e;
  --card: #102338;
  --card2: #132b45;
  --border: #23415f;
  --text: #e7f3ff;
  --muted: #8fb0ca;
  --accent: #38bdf8;
  --success: #22c55e;
  --warn: #f59e0b;
  --danger: #ef4444;
  --neutral: #94a3b8;
}
```

Cores semânticas:

```text
Conforme → verde
Não conforme → vermelho
Sem limite de referência → amarelo/âmbar
Neutro/informativo → azul
```

---

## Bibliotecas permitidas

Pode usar:

```text
HTML
CSS
JavaScript puro
Chart.js via CDN
```

Evitar frameworks pesados nesta fase.

Não usar React, Vue, Angular ou build tools sem autorização.

---

## Gráficos recomendados

### 1. Distribuição por status analítico

Tipo:

```text
donut ou barra horizontal
```

Dados:

```text
Conforme = 50
Não conforme = 7
Sem limite de referência = 15
```

### 2. Ranking de parâmetros críticos

Tipo:

```text
barra horizontal
```

Ordenação:

```text
total_nao_conformes DESC
```

### 3. Ranking de pontos críticos

Tipo:

```text
tabela ou barra horizontal
```

Ordenação:

```text
total_nao_conformes DESC
percentual_conformidade_com_limite ASC
```

### 4. Evolução mensal

Tipo:

```text
linha
```

Eixo X:

```text
competencia_coleta
```

Eixo Y:

```text
percentual_conformidade_com_limite
```

---

## Insights automáticos

O dashboard pode ter uma seção:

```text
Insights automáticos
```

Ela pode ser gerada localmente em JS com regras simples:

```text
- Se total_nao_conformes > 0, alertar quantidade.
- Se total_sem_limite_referencia > 0, alertar lacuna normativa.
- Se percentual_conformidade_com_limite < 90, indicar atenção técnica.
- Mostrar o parâmetro com maior número de não conformidades.
- Mostrar o ponto de coleta com maior número de não conformidades.
```

Integração com API de IA só deve ser usada se o usuário pedir explicitamente e nunca deve salvar chave no repositório.

---

## Regras de implementação

- `index.html` deve referenciar `css/style.css` e `js/app.js`.
- `app.js` deve buscar os JSONs via `fetch()`.
- Usar tratamento de erro se os JSONs não forem encontrados.
- Mostrar mensagem clara se os dados não carregarem.
- Não hardcodar os KPIs no HTML; carregar dos JSONs.
- Pode usar os valores oficiais apenas como validação, não como fonte fixa.
- O dashboard deve funcionar abrindo via servidor local simples.

---

## Servidor local para teste

Para evitar bloqueio de `fetch()` ao abrir arquivo direto, testar com:

```powershell
python -m http.server 8000
```

Abrir no navegador:

```text
http://localhost:8000/dashboard/
```

---

## Critérios de aceite

O dashboard está aprovado quando:

```text
1. Abre no navegador sem erro de console crítico
2. Carrega todos os JSONs em data/dashboard/
3. Mostra KPIs 72, 50, 7, 15, 69,44% e 87,72%
4. Mostra distribuição por status analítico
5. Mostra ranking de parâmetros críticos
6. Mostra ranking de pontos críticos
7. Mostra evolução mensal
8. Não contém senha, token, usuário de banco ou string de conexão
9. Está organizado em HTML, CSS e JS separados
```

---

## Narrativa para portfólio

Descrição recomendada:

```text
Após estruturar o pipeline de dados no Azure e disponibilizar views analíticas no Azure SQL, foi criado um dashboard HTML rápido consumindo JSONs exportados das views SQL. A solução simula uma entrega executiva emergencial, permitindo apresentar indicadores confiáveis em pouco tempo sem depender inicialmente de uma ferramenta tradicional de BI.
```
