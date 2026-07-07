# ADR-004 — Relatório Executivo com IA via Power Automate Visual

## 1. Status
Proposto

## 2. Contexto
O projeto precisa acionar uma automação dentro do Power BI para gerar um relatório executivo sob demanda a partir dos indicadores de qualidade da água, garantindo a segurança de credenciais e integrando capacidades de inteligência artificial.

## 3. Decisão
Decidir oficialmente que o acionamento da Fase 8 será feito por Power Automate Visual dentro do Power BI.

## 4. Alternativas consideradas
- JavaScript dentro do HTML Content
- fetch() dentro do HTML
- API key no DAX
- Power Automate Visual
- FastAPI local
- Azure Function direta
- Power Automate + Azure Function

## 5. Decisão escolhida
Power BI Power Automate Visual → Cloud Flow → Azure Function/endpoint seguro → IA → destino do relatório.

## 6. Consequências positivas
- Acionamento dentro do Power BI
- Melhor alinhamento com Azure/Power Platform
- Sem exposição de chave no dashboard
- Melhor narrativa de projeto corporativo
- Maior aprendizado em Power Platform

## 7. Consequências negativas
- Mais dependência de permissões Microsoft 365/Power Automate
- Retorno visual dentro do dashboard pode exigir persistência em outra fonte
- Pode depender de licenças/conectores
- Mais etapas de configuração

## 8. Regras de segurança
- Nunca colocar chave no Power BI
- Nunca colocar chave no DAX
- Nunca colocar chave no HTML
- Nunca passar segredo como campo do visual
- Usar Key Vault/variável segura para produção
- Validar permissões do flow

## 9. Próximo passo
Criar medidas auxiliares no Power BI para payload e iniciar flow mock via Power Automate Visual.
