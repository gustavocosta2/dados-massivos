"""Smoke test para validar integracao Spark + MinIO (S3A) + Apache Iceberg (JDBC Catalog)."""

from pyspark.sql import SparkSession


def main() -> None:
    """Executa escrita, leitura, checagem de snapshot e limpeza de tabela Iceberg."""
    spark = SparkSession.builder.appName("enem-iceberg-smoke-test").getOrCreate()

    spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg.enem_smoke")

    dados = [
        (2020, "MG", 1, 650.5),
        (2023, "SP", 0, None),
    ]
    colunas = ["NU_ANO", "SG_UF_PROVA", "IN_PRESENTE", "NU_NOTA_MT"]

    df = spark.createDataFrame(dados, colunas)
    df.writeTo("iceberg.enem_smoke.participantes_teste").using("iceberg").createOrReplace()

    resultado = spark.sql(
        "SELECT * FROM iceberg.enem_smoke.participantes_teste ORDER BY NU_ANO"
    )
    resultado.show()
    assert resultado.count() == 2, f"Esperado 2 registros, obtido {resultado.count()}"

    snapshots = spark.sql(
        "SELECT snapshot_id, operation FROM iceberg.enem_smoke.participantes_teste.snapshots"
    )
    snapshots.show()
    assert snapshots.count() >= 1, "Esperado ao menos 1 snapshot Iceberg."

    spark.sql("DROP TABLE IF EXISTS iceberg.enem_smoke.participantes_teste")
    spark.sql("DROP NAMESPACE IF EXISTS iceberg.enem_smoke")
    spark.stop()
    print("ICEBERG_SMOKE_TEST_OK")


if __name__ == "__main__":
    main()
