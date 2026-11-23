FROM apache/spark:3.5.3

USER root

ADD --chmod=0644 https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark/jars/hadoop-aws-3.3.4.jar
ADD --chmod=0644 https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar /opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar
ADD --chmod=0644 https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.2.1/delta-spark_2.12-3.2.1.jar /opt/spark/jars/delta-spark_2.12-3.2.1.jar
ADD --chmod=0644 https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.1/delta-storage-3.2.1.jar /opt/spark/jars/delta-storage-3.2.1.jar

USER spark
