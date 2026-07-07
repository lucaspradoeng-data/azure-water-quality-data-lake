# Skill 03 — Azure SQL para JSON do Dashboard

## Quando usar esta skill

Use esta skill para exportar as views analíticas do Azure SQL Database para arquivos JSON que serão consumidos pelo dashboard HTML.

Fluxo oficial:

```text
Azure SQL Views
  ↓
Python
  ↓
data/dashboard/*.json
  ↓
dashboard HTML
```

---

## Regras gerais

- O dashboard HTML não deve conectar diretamente no Azure SQL.
- A conexão com Azure SQL deve ocorrer apenas via Python local ou backend controlado.
- Credenciais devem ser lidas do `.env`.
- Nunca imprimir senha, token ou string de conexão completa.
- Nunca salvar credenciais em JSON, HTML, JS ou logs.
- Validar os arquivos JSON após exportar.

---

## Arquivo de ambiente esperado

Arquivo:

```text
.env
```

Variáveis esperadas:

```env
AZURE_SQL_SERVER=sql-awqdl-dev-lucas.database.windows.net
AZURE_SQL_DATABASE=sqldb-awqdl-dev
AZURE_SQL_USER=awqdladmin
AZURE_SQL_PASSWORD=SENHA_LOCAL_NAO_VERSIONADA
ODBC_DRIVER=ODBC Driver 18 for SQL Server
```

Regra: não alterar `.env` via agente.

---

## Views oficiais para exportação

Exportar exatamente estas views:

```text
dbo.vw_kpi_conformidade_geral
dbo.vw_conformidade_por_parametro
dbo.vw_conformidade_por_ponto_coleta
dbo.vw_evolucao_mensal_conformidade
dbo.vw_analise_conformidade
```

---

## Arquivos JSON de saída

Salvar em:

```text
data/dashboard/
```

Mapeamento oficial:

| View SQL | Arquivo JSON |
|---|---|
| `dbo.vw_kpi_conformidade_geral` | `kpi_conformidade_geral.json` |
| `dbo.vw_conformidade_por_parametro` | `conformidade_por_parametro.json` |
| `dbo.vw_conformidade_por_ponto_coleta` | `conformidade_por_ponto_coleta.json` |
| `dbo.vw_evolucao_mensal_conformidade` | `evolucao_mensal_conformidade.json` |
| `dbo.vw_analise_conformidade` | `analise_conformidade.json` |

---

## Estrutura JSON recomendada

Cada arquivo deve conter metadados mínimos:

```json
{
  "dataset": "nome_do_dataset",
  "generated_at": "YYYY-MM-DDTHH:MM:SS",
  "source": "dbo.nome_da_view",
  "row_count": 0,
  "records": []
}
```

Para datas, usar sempre:

```text
YYYY-MM-DD
```

Para números decimais, usar número JSON real, não texto.

---

## Script oficial esperado

Criar o script:

```text
scripts/exportar_views_dashboard.py
```

Responsabilidades do script:

```text
1. Ler variáveis do .env
2. Conectar no Azure SQL com pyodbc/SQLAlchemy
3. Consultar as views oficiais
4. Exportar cada view para JSON
5. Validar contagens oficiais
6. Exibir resumo no terminal
```

---

## Conexão recomendada

Usar o padrão ODBC que já foi validado no projeto:

```text
DRIVER={ODBC Driver 18 for SQL Server};
SERVER=tcp:sql-awqdl-dev-lucas.database.windows.net,1433;
DATABASE=sqldb-awqdl-dev;
UID=awqdladmin;
PWD=***;
Encrypt=yes;
TrustServerCertificate=yes;
Connection Timeout=60;
```

No SQLAlchemy, usar `odbc_connect` com `quote_plus`.

---

## Consultas de validação obrigatórias

Após exportar, validar:

```text
kpi_conformidade_geral.json:
  total_resultados = 72
  total_conformes = 50
  total_nao_conformes = 7
  total_sem_limite_referencia = 15
  total_com_limite_referencia = 57

analise_conformidade.json:
  row_count = 72

conformidade_por_parametro.json:
  row_count = 12

conformidade_por_ponto_coleta.json:
  row_count = 6
```

Se qualquer valor divergir, interromper a execução.

---

## Tipos de dados no JSON

### Datas

Converter para string ISO:

```text
YYYY-MM-DD
```

### Decimais

Converter para `float`.

### Inteiros

Converter para `int`.

### Nulos

Manter como `null`.

---

## Nomes de chaves recomendados

Para legibilidade no projeto HTML externo, usar nomes descritivos:

```text
total_resultados
total_conformes
total_nao_conformes
total_sem_limite_referencia
percentual_conformidade_geral
percentual_conformidade_com_limite
ponto_coleta
parametro
status_analitico
competencia_coleta
```

Não é necessário usar chaves minificadas, pois o HTML não ficará dentro de uma medida DAX do Power BI.

---

## Critério de aceite

A exportação está correta quando:

```text
1. Todos os JSONs existem em data/dashboard/
2. Nenhum JSON contém credenciais
3. Os row_counts batem com os valores esperados
4. Os KPIs batem com 72, 50, 7, 15, 57, 69,44 e 87,72
5. O terminal exibe resumo claro da exportação
```
