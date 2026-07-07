from pathlib import Path
import os
import json
from decimal import Decimal
from datetime import date, datetime, time

import pyodbc
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = BASE_DIR / "data" / "dashboard"


EXPORTACOES = [
    {
        "arquivo": "kpi_conformidade_geral.json",
        "sql": """
            SELECT *
            FROM dbo.vw_kpi_conformidade_geral;
        """,
    },
    {
        "arquivo": "conformidade_por_parametro.json",
        "sql": """
            SELECT *
            FROM dbo.vw_conformidade_por_parametro
            ORDER BY
                total_nao_conformes DESC,
                percentual_nao_conformidade_com_limite DESC,
                parametro;
        """,
    },
    {
        "arquivo": "conformidade_por_ponto_coleta.json",
        "sql": """
            SELECT *
            FROM dbo.vw_conformidade_por_ponto_coleta
            ORDER BY
                total_nao_conformes DESC,
                percentual_conformidade_com_limite ASC,
                ponto_coleta;
        """,
    },
    {
        "arquivo": "evolucao_mensal_conformidade.json",
        "sql": """
            SELECT *
            FROM dbo.vw_evolucao_mensal_conformidade
            ORDER BY competencia_coleta;
        """,
    },
    {
        "arquivo": "analise_conformidade.json",
        "sql": """
            SELECT *
            FROM dbo.vw_analise_conformidade
            ORDER BY id_resultado;
        """,
    },
]


def criar_conexao():
    load_dotenv(BASE_DIR / ".env")

    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE")
    user = os.getenv("AZURE_SQL_USER")
    password = os.getenv("AZURE_SQL_PASSWORD")
    driver = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

    if not all([server, database, user, password]):
        raise ValueError("Arquivo .env incompleto. Verifique servidor, banco, usuário e senha.")

    connection_string = (
        f"DRIVER={{{driver}}};"
        f"SERVER=tcp:{server},1433;"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=60;"
    )

    return pyodbc.connect(connection_string)


def converter_valor(valor):
    if isinstance(valor, Decimal):
        return float(valor)

    if isinstance(valor, datetime):
        return valor.isoformat()

    if isinstance(valor, date):
        return valor.isoformat()

    if isinstance(valor, time):
        return valor.strftime("%H:%M:%S")

    return valor


def consultar_view(conn, sql: str):
    cursor = conn.cursor()
    cursor.execute(sql)

    colunas = [coluna[0] for coluna in cursor.description]

    registros = []
    for linha in cursor.fetchall():
        registro = {
            coluna: converter_valor(valor)
            for coluna, valor in zip(colunas, linha)
        }
        registros.append(registro)

    return registros


def salvar_json(nome_arquivo: str, dados: list[dict]):
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    caminho_saida = DASHBOARD_DIR / nome_arquivo

    with caminho_saida.open("w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    return caminho_saida


def main():
    print("Exportando views do Azure SQL para JSON...")
    print(f"Destino: {DASHBOARD_DIR}")

    with criar_conexao() as conn:
        print("Conexão com Azure SQL validada com sucesso.")

        for item in EXPORTACOES:
            nome_arquivo = item["arquivo"]
            sql = item["sql"]

            dados = consultar_view(conn, sql)
            salvar_json(nome_arquivo, dados)

            print(f"{nome_arquivo}: {len(dados)} registros")

    print("\nExportação finalizada com sucesso.")


if __name__ == "__main__":
    main()