# Fase 8.1.2 — Azure Function HTTP Mock

## Objetivo
Esta Azure Function serve como um endpoint HTTP mock para receber as métricas agregadas do dashboard do Azure Water Quality Data Lake via query string, retornando um relatório executivo formatado em HTML ou JSON, sem depender do Power Automate.

## Estrutura
- `function_app.py`: Contém a lógica principal da Function (v2 programming model).
- `host.json`: Configurações do host do Azure Functions.
- `local.settings.json`: Configurações de ambiente para execução local (não versionado).

## Como executar localmente
1. Certifique-se de ter o Azure Functions Core Tools instalado.
2. Navegue até este diretório (`azure-functions/awqdl-report-mock`).
3. Instale as dependências: `pip install -r requirements.txt` (sugere-se usar um `.venv`).
4. Inicie a Function localmente: `func start`

## Exemplos de URLs de Teste Local

**HTML (Padrão):**
http://localhost:7071/api/relatorio-awqdl?formato=html

**JSON:**
http://localhost:7071/api/relatorio-awqdl?formato=json

**Com parâmetros:**
http://localhost:7071/api/relatorio-awqdl?total_resultados=72&total_conformes=50&total_nao_conformes=7&total_sem_limite=15&total_com_limite=57&percentual_conformidade_geral=69.44&percentual_conformidade_com_limite=87.72&risco_nao_conformidade_com_limite=12.28&formato=html

## Aviso de Segurança
Este mock NÃO executa integrações com IA, banco de dados ou Key Vault. Nenhum segredo, API key ou string de conexão deve ser inserido neste código.
