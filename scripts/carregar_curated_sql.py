from pathlib import Path
import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parents[1]
CURATED_DIR = BASE_DIR / "data" / "curated"

ARQUIVOS_CARGA = [
    ("dbo.dim_ponto_coleta", CURATED_DIR / "dimensoes" / "dim_ponto_coleta.csv"),
    ("dbo.dim_parametro", CURATED_DIR / "dimensoes" / "dim_parametro.csv"),
    ("dbo.dim_responsavel", CURATED_DIR / "dimensoes" / "dim_responsavel.csv"),
    ("dbo.dim_amostra", CURATED_DIR / "dimensoes" / "dim_amostra.csv"),
    ("dbo.fato_resultado_qualidade", CURATED_DIR / "fatos" / "fato_resultado_qualidade.csv"),
]


def criar_engine():
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

    params = quote_plus(connection_string)

    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        fast_executemany=True,
    )


def ler_csv(caminho: Path) -> pd.DataFrame:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig")

    df = df.astype(object).where(pd.notna(df), None)

    for coluna in ["possui_limite_referencia", "indicador_nao_conforme"]:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(
                lambda valor: None if valor is None else int(float(valor))
            )

    return df


def limpar_tabelas(engine):
    comandos = [
        "DELETE FROM dbo.fato_resultado_qualidade;",
        "DELETE FROM dbo.dim_amostra;",
        "DELETE FROM dbo.dim_parametro;",
        "DELETE FROM dbo.dim_ponto_coleta;",
        "DELETE FROM dbo.dim_responsavel;",
    ]

    with engine.begin() as conn:
        for comando in comandos:
            conn.execute(text(comando))


def carregar_tabela(engine, nome_tabela: str, caminho_csv: Path):
    schema, tabela = nome_tabela.split(".")

    df = ler_csv(caminho_csv)

    df.to_sql(
        name=tabela,
        con=engine,
        schema=schema,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

    print(f"Tabela carregada: {nome_tabela} | registros: {len(df)}")


def validar_carga(engine):
    consulta = """
    SELECT 'dim_ponto_coleta' AS tabela, COUNT(*) AS registros FROM dbo.dim_ponto_coleta
    UNION ALL
    SELECT 'dim_parametro', COUNT(*) FROM dbo.dim_parametro
    UNION ALL
    SELECT 'dim_responsavel', COUNT(*) FROM dbo.dim_responsavel
    UNION ALL
    SELECT 'dim_amostra', COUNT(*) FROM dbo.dim_amostra
    UNION ALL
    SELECT 'fato_resultado_qualidade', COUNT(*) FROM dbo.fato_resultado_qualidade;
    """

    with engine.connect() as conn:
        resultado = conn.execute(text(consulta)).fetchall()

    print("\nValidação da carga:")
    for linha in resultado:
        print(f"{linha.tabela}: {linha.registros}")


def main():
    print("Iniciando carga curated para Azure SQL...")

    engine = criar_engine()

    print("Testando conexão real com Azure SQL...")

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("Conexão real com Azure SQL validada com sucesso.")
    print("Limpando tabelas antes da carga...")

    limpar_tabelas(engine)

    print("Carregando arquivos CSV...")

    for nome_tabela, caminho_csv in ARQUIVOS_CARGA:
        carregar_tabela(engine, nome_tabela, caminho_csv)

    validar_carga(engine)

    print("\nCarga finalizada com sucesso.")


if __name__ == "__main__":
    main()