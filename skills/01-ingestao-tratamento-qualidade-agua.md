# Skill 01 — Ingestão e Tratamento de Dados de Qualidade da Água

## Quando usar esta skill

Use esta skill sempre que precisar importar, reconhecer, limpar, validar ou transformar dados de qualidade da água no projeto **Azure Water Quality Data Lake**.

Esta skill cobre:

```text
raw → processed → curated
```

Ferramentas preferenciais:

```text
Python
pandas
arquivos CSV
Azure Data Lake
Azure SQL Database
```

Não usar Power Query como ferramenta principal nesta fase, salvo pedido explícito.

---

## Princípio central

O dado bruto nunca deve ser alterado.

```text
raw        = fonte original preservada
processed  = dado limpo e padronizado
curated    = dado estruturado para análise e SQL
```

Regra crítica:

```text
Nunca sobrescrever arquivos em data/raw.
Nunca alterar diretamente lake/raw.
Toda transformação deve gerar novo arquivo em processed ou curated.
```

---

## Dataset oficial inicial

Arquivo bruto original:

```text
data/raw/dados_conformidade_v2_1_0.csv
```

Características reconhecidas:

```text
Formato: CSV
Separador: ;
Cabeçalho: ausente no raw
Linhas: 72
Colunas: 30
Amostras: 6
Parâmetros: 12
```

Indicadores esperados:

```text
Conformes: 50
Não conformes: 7
Sem limite de referência: 15
Com limite de referência: 57
```

---

## Contrato de dados do arquivo raw

Aplicar estes nomes de colunas ao CSV bruto sem cabeçalho:

```text
resultado_id
amostra_id
codigo_amostra
data_coleta
hora_coleta
tipo_ponto_id
tipo_ponto
ponto_coleta_id
ponto_coleta
categoria_ponto
municipio
uf
tecnico_id
tecnico_nome
status_amostra_id
status_amostra
parametro_id
parametro_nome
grupo_parametro
valor_resultado
unidade_medida
data_resultado
metodo_analise
limite_id
limite_minimo
limite_maximo
descricao_limite
status_conformidade
possui_limite
fora_limite
```

---

## Regras de limpeza para processed

### 1. Leitura do CSV

Usar:

```python
pd.read_csv(caminho, sep=';', header=None, encoding='utf-8-sig')
```

Se `utf-8-sig` falhar, testar `utf-8`.

### 2. Aplicar cabeçalho oficial

Atribuir exatamente as 30 colunas do contrato de dados.

Se a quantidade de colunas for diferente de 30, interromper o processo e exibir erro claro.

### 3. Tratar nulos

Converter valores textuais nulos para nulo real:

```text
NULL
null
None
""
```

### 4. Padronizar datas

Campos:

```text
data_coleta
data_resultado
```

Converter para data no formato ISO:

```text
YYYY-MM-DD
```

### 5. Padronizar hora

Campo:

```text
hora_coleta
```

Converter para:

```text
HH:MM:SS
```

### 6. Padronizar números decimais

Campos:

```text
valor_resultado
limite_minimo
limite_maximo
```

Regras:

```text
aceitar ponto decimal
aceitar vírgula decimal se aparecer
converter para decimal
preservar nulo quando não houver limite
```

### 7. Padronizar flags booleanas

Campos:

```text
possui_limite
fora_limite
```

Converter para:

```text
1 = verdadeiro
0 = falso
NULL = não aplicável
```

---

## Regras de validação do processed

Após gerar `dados_conformidade_processado.csv`, validar:

```text
Total de linhas = 72
Total de colunas = 30
Amostras únicas = 6
Parâmetros únicos = 12
Conformes = 50
Não conformes = 7
Sem limite de referência = 15
Com limite de referência = 57
```

Se qualquer número divergir, interromper e reportar.

---

## Camada curated

A camada curated deve transformar a tabela processada em modelo analítico:

```text
dim_ponto_coleta.csv
dim_parametro.csv
dim_responsavel.csv
dim_amostra.csv
fato_resultado_qualidade.csv
analise_conformidade_curated.csv
```

### Diretórios oficiais

```text
data/curated/dimensoes/dim_ponto_coleta.csv
data/curated/dimensoes/dim_parametro.csv
data/curated/dimensoes/dim_responsavel.csv
data/curated/dimensoes/dim_amostra.csv
data/curated/fatos/fato_resultado_qualidade.csv
data/curated/bi/analise_conformidade_curated.csv
```

---

## Modelo curated esperado

### dim_ponto_coleta

```text
id_ponto_coleta
ponto_coleta
tipo_ponto
municipio
estado
```

Resultado esperado:

```text
6 registros
```

### dim_parametro

```text
id_parametro
parametro
categoria_parametro
unidade_medida
```

Resultado esperado:

```text
12 registros
```

### dim_responsavel

```text
id_responsavel
responsavel
```

Resultado esperado:

```text
4 registros
```

### dim_amostra

```text
id_amostra
codigo_amostra
data_coleta
hora_coleta
id_tipo_amostra
tipo_amostra
id_ponto_coleta
id_responsavel
id_status
status_amostra
```

Resultado esperado:

```text
6 registros
```

### fato_resultado_qualidade

```text
id_resultado
id_amostra
id_ponto_coleta
id_parametro
id_responsavel
data_coleta
data_analise
valor_resultado
id_limite
valor_minimo
valor_maximo
referencia_normativa
classificacao_resultado
possui_limite_referencia
indicador_nao_conforme
metodo_analise
```

Resultado esperado:

```text
72 registros
```

---

## Regras críticas

- Não criar dimensões novas sem autorização.
- Não renomear colunas oficiais sem autorização.
- Não alterar nomes de tabelas SQL oficiais.
- Não transformar registros sem limite em conformes.
- Não calcular percentual de conformidade técnica usando registros sem limite como denominador.
- Sempre validar contagens antes de avançar para SQL ou dashboard.
