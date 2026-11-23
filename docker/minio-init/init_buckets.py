"""Inicializa os buckets padrao do Lakehouse no MinIO."""

import os
import time
from minio import Minio

ENDPOINT = os.environ.get("MINIO_ENDPOINT", "enem-minio:9000").replace("http://", "")
ACCESS_KEY = os.environ.get("MINIO_ROOT_USER", "enem_minio")
SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD", "enem_minio_pass")
BUCKETS = ["bronze", "silver", "gold", "warehouse"]


def main() -> None:
    client = Minio(ENDPOINT, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

    for attempt in range(1, 31):
        try:
            client.list_buckets()
            break
        except Exception as exc:
            print(f"Aguardando MinIO ({attempt}/30): {exc}")
            time.sleep(2)
    else:
        raise RuntimeError("MinIO nao respondeu a tempo.")

    for bucket in BUCKETS:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            print(f"Bucket criado: {bucket}")
        else:
            print(f"Bucket ja existe: {bucket}")


if __name__ == "__main__":
    main()
