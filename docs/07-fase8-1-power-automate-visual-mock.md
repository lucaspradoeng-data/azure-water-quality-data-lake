# Fase 8.1 — Power Automate Visual + Cloud Flow Mock

> [!WARNING]
> **Status: Bloqueado no ambiente atual por limitação de conta Power Automate**
> A execução real com Power Automate Visual depende de conta corporativa/escolar e ficará como caminho enterprise futuro.

## 1. Objetivo
O objetivo desta fase é validar o acionamento de uma automação diretamente dentro do Power BI utilizando o Power Automate Visual. O intuito é demonstrar que o dashboard pode capturar as métricas consolidadas e acionar fluxos de trabalho sob demanda, sem expor chaves ou segredos.

## 2. Escopo
Nesta fase, o escopo é estritamente de validação e mock. **Não há IA real, Azure Function ou integração com API externa.** O fluxo irá apenas receber os dados do Power BI e simular a geração de um relatório executivo, enviando um texto estático e o payload recebido via e-mail ou Teams.

## 3. Medidas DAX criadas
Foram criadas medidas específicas para extrair os dados e o contexto do dashboard:
- PA Timestamp Execucao AWQDL
- PA Assunto Relatorio AWQDL
- PA Resumo Executivo Mock AWQDL
- PA Payload JSON AWQDL
- PA Parametros Criticos Texto AWQDL
- PA Pontos Criticos Texto AWQDL

## 4. Como inserir o Power Automate Visual no Power BI
Para incorporar a automação no dashboard, siga as instruções:
- Abra a página do dashboard.
- Insira o visual Power Automate na tela.
- Adicione os seguintes campos/medidas no visual:
  - PA Assunto Relatorio AWQDL
  - PA Resumo Executivo Mock AWQDL
  - PA Payload JSON AWQDL
  - PA Parametros Criticos Texto AWQDL
  - PA Pontos Criticos Texto AWQDL

## 5. Como criar o Cloud Flow mock
O fluxo conceitual no Power Automate segue a seguinte estrutura:
- **Trigger:** Power BI button clicked
- **Ação:** Compose com payload recebido
- **Ação:** Enviar email para o usuário
- **Assunto:** PA Assunto Relatorio AWQDL
- **Corpo:** PA Resumo Executivo Mock AWQDL + Payload JSON

## 6. Destino recomendado nesta fase
Para validação rápida nesta etapa, recomendamos configurar o destino do fluxo para envio via **email Outlook** ou mensagem direta no **Teams**.

## 7. Critérios de aceite
- [ ] Botão aparece no Power BI.
- [ ] Flow é acionado pelo Power Automate Visual.
- [ ] Flow recebe dados do relatório.
- [ ] Email/Teams recebe relatório mock.
- [ ] Nenhuma chave é exposta.
- [ ] Nenhuma chamada de IA é feita.
- [ ] Dashboard original permanece funcionando.

## 8. Próxima fase
A **Fase 8.2** consistirá na implementação de um **Azure Function mock** ou endpoint seguro para iniciar a arquitetura real de back-end.
