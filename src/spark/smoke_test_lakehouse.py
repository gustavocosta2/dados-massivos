"""Smoke test para validar integracao Spark + MinIO (S3A) + Hive Metastore."""

from pyspark.sql import SparkSession


def main() -> None:
    """Executa escrita, leitura e limpeza de tabela de teste no Lakehouse."""
    spark = (
        SparkSession.builder.appName("enem-lakehouse-smoke-test")
        .enableHiveSupport()
        .getOrCreate()
    )

    spark.sql("CREATE DATABASE IF NOT EXISTS enem_smoke")

    dados = [
        (2020, "MG", 1, 650.5),
        (2023, "SP", 0, None),
    ]
    colunas = ["NU_ANO", "SG_UF_PROVA", "IN_PRESENTE", "NU_NOTA_MT"]

    df = spark.createDataFrame(dados, colunas)
    df.write.mode("overwrite").format("parquet").option(
        "path", "s3a://silver/smoke_test_participantes"
    ).saveAsTable("enem_smoke.participantes_teste")

    resultado = spark.sql("SELECT * FROM enem_smoke.participantes_teste ORDER BY NU_ANO")
    resultado.show()
    assert resultado.count() == 2, f"Esperado 2 registros, obtido {resultado.count()}"

    spark.sql("DROP TABLE IF EXISTS enem_smoke.participantes_teste")
    spark.sql("DROP DATABASE IF EXISTS enem_smoke")
    spark.stop()
    print("SMOKE_TEST_OK")


if __name__ == "__main__":
    main()
