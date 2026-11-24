FROM apache/spark:3.5.3

USER root

ADD --chmod=0644 https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark/jars/hadoop-aws-3.3.4.jar
ADD --chmod=0644 https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar /opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar
ADD --chmod=0644 https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.7.1/iceberg-spark-runtime-3.5_2.12-1.7.1.jar /opt/spark/jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar
ADD --chmod=0644 https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar /opt/spark/jars/postgresql-42.7.3.jar

USER spark
