FROM python:3.11-alpine

RUN pip install --no-cache-dir minio

COPY init_buckets.py /init_buckets.py

CMD ["python", "/init_buckets.py"]
