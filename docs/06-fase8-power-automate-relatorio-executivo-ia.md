# Fase 8 — Relatório Executivo com IA via Power Automate Visual

## 1. Objetivo da fase
A Fase 8 busca transformar os indicadores do dashboard AWQDL em uma síntese executiva automática acionada diretamente dentro do Power BI.

## 2. Contexto atual
- A v1.0 Executive Dashboard está validada.
- O botão "Gerar Relatório Executivo" no HTML Content é apenas placeholder visual.
- O dashboard oficial roda dentro do Power BI via HTML Content.
- O acionamento oficial da Fase 8 será feito por um Power Automate Visual.
- Chaves de IA não podem ficar no DAX, HTML ou Power BI.

## 3. Arquitetura oficial proposta

```mermaid
flowchart TD
    A[Power BI Dashboard] --> B[Power Automate Visual]
    B --> C[Cloud Flow "Gerar Relatório Executivo"]
    C --> D[Azure Function ou HTTP endpoint seguro]
    D --> E[Variável de ambiente / Key Vault]
    E --> F[Modelo de IA]
    F --> G[Destino do relatório]
```

Destinos possíveis:
- Email executivo
- Teams
- SharePoint/OneDrive
- Azure SQL
- Dataverse

## 4. Justificativa da escolha Power Automate Visual
- Acionamento ocorre dentro do Power BI.
- Permite demonstrar automação sob demanda.
- Permite passar dados contextuais do relatório para o flow.
- Mantém o Power BI como camada central.
- Evita expor chave de IA no HTML/DAX.
- Aumenta aprendizado em Power Platform e Azure.

## 5. Limitação técnica importante
- O Power Automate Visual aciona um flow.
- O retorno do texto gerado não necessariamente aparece automaticamente dentro do HTML Content.
- Para exibir o relatório gerado no Power BI, será necessário gravar o resultado em uma fonte de dados, como Azure SQL/Dataverse/SharePoint, e então atualizar ou consultar essa fonte.
- Para a primeira versão, o relatório pode ser enviado por email/Teams ou salvo em SharePoint.

## 6. Alternativas de destino do relatório

| Destino | Vantagem | Limitação | Recomendação |
|---|---|---|---|
| Email Outlook | Entrega direta ao usuário final | Difícil voltar para o Power BI | Alta (para demonstração) |
| Microsoft Teams | Entrega imediata no chat/canal | Requer app do Teams | Alta (para demonstração) |
| SharePoint | Persistência do relatório em lista/documento | Atualização no Power BI requer refresh | Alta |
| OneDrive | Salva o arquivo fisicamente | Menos estruturado | Média |
| Azure SQL | Estrutura relacional, Power BI já lê via DirectQuery | Requer desenvolvimento na Azure Function para insert | Alta (Evolução) |
| Dataverse | Nativo da Power Platform, muito integrado | Pode exigir licença Premium | Média |

## 7. Arquitetura recomendada para demonstração
Power BI → Power Automate Visual → Cloud Flow → Azure Function mock ou HTTP mock → relatório enviado por email/Teams.

## 8. Arquitetura recomendada para evolução Azure
Power BI → Power Automate Visual → Cloud Flow → Azure Function → Key Vault → Azure OpenAI/OpenAI → Azure SQL/SharePoint → Power BI.

## 9. Campos que o Power Automate Visual deve receber
- Total Resultados
- Total Conformes
- Total Nao Conformes
- Total Sem Limite Referencia
- Total Com Limite Referencia
- Percentual Conformidade Geral
- Percentual Conformidade Com Limite
- Risco Nao Conformidade Com Limite
- Parametros Criticos
- Pontos Criticos

## 10. Payload conceitual
```json
{
  "projeto": "Azure Water Quality Data Lake",
  "total_resultados": 72,
  "total_conformes": 50,
  "total_nao_conformes": 7,
  "total_sem_limite": 15,
  "total_com_limite": 57,
  "percentual_conformidade_geral": 69.44,
  "percentual_conformidade_com_limite": 87.72,
  "risco_nao_conformidade_com_limite": 12.28,
  "parametros_criticos": [],
  "pontos_criticos": []
}
```

## 11. Resposta esperada
- Resumo operacional
- Pontos críticos
- Riscos
- Recomendações operacionais
- Próximos passos

## 12. Segurança
- API key nunca entra no Power BI.
- API key nunca entra no DAX.
- API key nunca entra no HTML.
- O flow não deve armazenar segredo em texto aberto.
- Em demonstração, usar variável protegida/conexão segura.
- Em produção, usar Azure Key Vault.

## 13. Riscos e controles

| Risco | Impacto | Controle |
|---|---|---|
| Exposição de chave | Alto | Usar Azure Function/Key Vault, nunca em frontend |
| Envio de dados sensíveis | Médio | Payload envia apenas sumarizações agregadas (KPIs) |
| Flow sem permissão | Alto | Configurar credenciais de execução e conectores adequadamente |
| Limitação de retorno visual no Power BI | Médio | Enviar para Teams/Email primeiro, depois avaliar gravação em BD + DirectQuery |
| Dependência de licenças/conectores | Médio | Validar se os conectores padrão do Office 365 atendem ou se precisa de Premium |

## 14. Roadmap técnico da Fase 8
- 8.1 Criar branch da Fase 8
- 8.2 Documentar arquitetura Power Automate Visual
- 8.3 Criar medidas DAX auxiliares para payload do flow
- 8.4 Inserir Power Automate Visual no Power BI
- 8.5 Criar Cloud Flow com trigger do Power BI
- 8.6 Testar flow com payload fixo
- 8.7 Enviar relatório mock por email/Teams
- 8.8 Criar Azure Function mock
- 8.9 Integrar Azure Function ao flow
- 8.10 Adicionar IA com segredo protegido
- 8.11 Persistir relatório em SharePoint/Azure SQL
- 8.12 Atualizar documentação e release futura

## 15. Critérios de aceite
- [ ] Power Automate Visual inserido no Power BI
- [ ] Flow acionado pelo botão dentro do relatório
- [ ] Campos do Power BI recebidos no flow
- [ ] Relatório mock gerado
- [ ] Nenhuma chave exposta no Power BI
- [ ] Nenhuma chave exposta no DAX
- [ ] Nenhuma chave exposta no HTML
- [ ] Resultado enviado/salvo em destino definido
- [ ] Documentação atualizada
