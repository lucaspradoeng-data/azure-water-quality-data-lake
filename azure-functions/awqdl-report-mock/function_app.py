import azure.functions as func
import logging
import json
import html

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="relatorio-awqdl", methods=["GET"])
def relatorio_awqdl(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processando requisição de relatório executivo mock.')

    # 1. Recuperar e sanitizar parâmetros (com fallback para valores oficiais da v1.0)
    try:
        total_resultados = int(req.params.get('total_resultados', 72))
        total_conformes = int(req.params.get('total_conformes', 50))
        total_nao_conformes = int(req.params.get('total_nao_conformes', 7))
        total_sem_limite = int(req.params.get('total_sem_limite', 15))
        total_com_limite = int(req.params.get('total_com_limite', 57))
        
        perc_geral = float(req.params.get('percentual_conformidade_geral', 69.44))
        perc_limite = float(req.params.get('percentual_conformidade_com_limite', 87.72))
        risco = float(req.params.get('risco_nao_conformidade_com_limite', 12.28))
    except ValueError:
        return func.HttpResponse(
            "Erro: Parâmetros numéricos inválidos.",
            status_code=400
        )

    formato = req.params.get('formato', 'html').lower()
    if formato not in ['html', 'json']:
        formato = 'html'

    # Texto do resumo gerado
    resumo = (
        f"De {total_resultados} resultados analisados, {total_conformes} estão conformes, "
        f"{total_nao_conformes} apresentam não conformidade e {total_sem_limite} não possuem limite de referência. "
        f"A conformidade geral é de {perc_geral}%, enquanto a conformidade considerando apenas parâmetros com limite é de {perc_limite}%. "
        f"O risco de não conformidade sobre resultados com limite é de {risco}%."
    )

    if formato == 'json':
        dados_json = {
            "projeto": "Azure Water Quality Data Lake",
            "fase": "8.1.2",
            "tipo": "relatorio_executivo_mock",
            "indicadores": {
                "total_resultados": total_resultados,
                "total_conformes": total_conformes,
                "total_nao_conformes": total_nao_conformes,
                "total_sem_limite": total_sem_limite,
                "total_com_limite": total_com_limite,
                "percentual_conformidade_geral": perc_geral,
                "percentual_conformidade_com_limite": perc_limite,
                "risco_nao_conformidade_com_limite": risco
            },
            "resumo": resumo,
            "mock": True
        }
        return func.HttpResponse(
            json.dumps(dados_json, ensure_ascii=False),
            mimetype="application/json",
            status_code=200
        )

    # HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório Executivo AWQDL</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f3f2f1; color: #323130; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #0078d4; margin-bottom: 5px; }}
            h2 {{ color: #605e5c; font-weight: normal; margin-top: 0; font-size: 1.2em; }}
            .cards {{ display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0; }}
            .card {{ background: #f3f2f1; padding: 15px; border-radius: 6px; flex: 1; min-width: 120px; text-align: center; border-bottom: 3px solid #0078d4; }}
            .card.nc {{ border-bottom-color: #d13438; }}
            .card h3 {{ margin: 0; font-size: 0.9em; color: #605e5c; text-transform: uppercase; }}
            .card p {{ margin: 10px 0 0; font-size: 1.8em; font-weight: bold; color: #323130; }}
            .section {{ margin-top: 30px; }}
            .section h3 {{ color: #0078d4; border-bottom: 1px solid #edebe9; padding-bottom: 5px; }}
            .warning {{ background: #fff4ce; border-left: 4px solid #f2c811; padding: 10px; margin-top: 30px; font-size: 0.9em; color: #323130; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Relatório Executivo AWQDL</h1>
            <h2>Azure Water Quality Data Lake</h2>
            
            <div class="cards">
                <div class="card">
                    <h3>Resultados</h3>
                    <p>{total_resultados}</p>
                </div>
                <div class="card">
                    <h3>Conformes</h3>
                    <p>{total_conformes}</p>
                </div>
                <div class="card nc">
                    <h3>Não Conformes</h3>
                    <p>{total_nao_conformes}</p>
                </div>
                <div class="card">
                    <h3>Conf. Geral</h3>
                    <p>{perc_geral}%</p>
                </div>
            </div>

            <div class="section">
                <h3>Resumo Operacional</h3>
                <p>{html.escape(resumo)}</p>
            </div>

            <div class="section">
                <h3>Pontos de Atenção</h3>
                <ul>
                    <li>A taxa de conformidade com limite está em {perc_limite}%.</li>
                    <li>Há {total_nao_conformes} análises que demandam ação imediata.</li>
                </ul>
            </div>

            <div class="section">
                <h3>Recomendações Mock</h3>
                <p>Priorizar a investigação das não conformidades identificadas. <i>(Nota: Esta é uma recomendação estática para fins de validação técnica)</i>.</p>
            </div>

            <div class="warning">
                <strong>Aviso:</strong> Relatório mock gerado para validação da Fase 8.1.2. Não utiliza IA real.
            </div>
        </div>
    </body>
    </html>
    """
    
    return func.HttpResponse(
        html_content,
        mimetype="text/html",
        status_code=200
    )
