# ADR-005 — Fallback Power BI Button + Azure Function HTTP Mock

## 1. Status
Proposto

## 2. Contexto
O Power Automate Visual é a arquitetura enterprise planejada, mas está bloqueado no ambiente atual pela ausência de conta corporativa/escolar.

## 3. Decisão
Adotar temporariamente Power BI Button + Web URL dinâmica + Azure Function HTTP Mock para validar acionamento dentro do Power BI.

## 4. Alternativas consideradas
- Power Automate Visual
- Power BI Button + Azure Function
- HTML Content com JavaScript/fetch
- execução manual externa
- FastAPI local

## 5. Justificativa
O fallback mantém:
- acionamento dentro do Power BI
- aprendizado Azure
- segurança
- simplicidade
- compatibilidade com ambiente atual

## 6. Consequências positivas
- não depende de Power Automate
- mantém demonstração dentro do Power BI
- fortalece aprendizado Azure Function
- evita expor chave
- facilita PoC rápida

## 7. Consequências negativas
- não envia email/Teams automaticamente
- pode abrir navegador externo
- retorno não fica embutido no dashboard
- menos enterprise que Power Automate
- precisa de Azure Function publicada

## 8. Regras de segurança
- nunca usar function key no DAX
- nunca usar API key no DAX
- nunca passar segredo na URL
- usar somente dados agregados
- produção futura deve usar APIM/Key Vault/autenticação adequada

## 9. Próximo passo
Criar Azure Function HTTP mock que retorne relatório executivo HTML/JSON com dados agregados.
