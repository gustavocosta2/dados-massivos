# Etapas do Trabalho — Processamento de Dados Massivos (ENEM 2020–2023)

Documento de acompanhamento das etapas do projeto **Lakehouse + Predição de Abstenção no ENEM (2020–2023)**, desenvolvido por **Gustavo Costa** e **João Paulo**.

> **Pergunta central:** Como a abstenção e o desempenho por área e redação variaram entre 2020–2023 por renda, raça/cor, sexo e trajetória escolar, e quais fatores socioeconômicos prévios mais aumentam o risco de ausência no exame?

---

## Etapa 0 — Definição do Escopo, Objetivo e Arquitetura *(Concluída)*
- [x] Selecionar base pública com volume > 5 GB (`Microdados do ENEM 2020–2023`, ~6,88 GB descompactados e 16,58M registros).
- [x] Refinar o Objetivo Geral e os Objetivos Específicos (análise descritiva + modelo preditivo de risco de abstenção no Spark MLlib).
- [x] Definir a arquitetura Medalhão (*Bronze → Silver → Gold*) com **MinIO**, **Apache Iceberg**, **Apache Spark**, **Apache Airflow (Standalone)** e **Streamlit**.
- [x] Atualizar o documento de caracterização e proposta ([caracterizacao_microdados_enem_2020-2023.pdf](caracterizacao_microdados_enem_2020-2023.pdf)) e o [README.md](../README.md).

---

## Etapa 1 — Infraestrutura Base em Docker *(Concluída)*
- [x] Configurar `docker-compose.yml` com containers nomeados de forma legível (`enem-postgres`, `enem-minio`, `enem-minio-init`, `enem-spark-master`, `enem-spark-worker`, `enem-airflow`).
- [x] Configurar integração Spark + MinIO (`s3a://`) + **Apache Iceberg** (JDBC Catalog no PostgreSQL).
- [x] Adicionar **Apache Airflow** em modo `standalone` (`enem-airflow`) conectado ao PostgreSQL.
- [x] Criar automaticamente os buckets `bronze`, `silver`, `gold` e `warehouse`.
- [x] Validar o ambiente com o *smoke test* do Iceberg ([src/spark/smoke_test_lakehouse.py](../src/spark/smoke_test_lakehouse.py)).

---

## Etapa 2 — Ingestão dos Dados Brutos (Camada Bronze)
- [ ] Mapear os links/arquivos oficiais dos pacotes do INEP (2020, 2021, 2022 e 2023).
- [ ] Implementar script Python de ingestão (download, descompactação e validação de integridade dos CSVs e dicionários).
- [ ] Enviar os CSVs brutos (`MICRODADOS_ENEM_ano.csv`) para `s3a://bronze/enem/ano=<ANO>/` no MinIO.
- [ ] Gerar uma amostra reduzida local (ex.: 100 mil linhas por ano) para agilizar desenvolvimento e testes antes da execução completa.
- [ ] Adicionar testes unitários para a etapa de ingestão.

---

## Etapa 3 — Limpeza, Harmonização e Catálogo Iceberg (Camada Silver)
- [ ] Comparar os dicionários de 2020 a 2023 para mapear mudanças de categorias (ex.: faixas de renda `Q006` e `TP_ANO_CONCLUIU`).
- [ ] Implementar job PySpark (`bronze -> silver`) para:
  - [ ] Tratar *encoding* (`latin1`), separador (`;`) e tipagem das 76 colunas.
  - [ ] Harmonizar as variáveis que mudam entre edições.
  - [ ] Criar flags derivadas de abstenção (ex.: `IN_AUSENTE_TOTAL`, `IN_AUSENTE_PARCIAL`).
- [ ] Gravar os dados limpos como tabela **Apache Iceberg** particionada por `NU_ANO` (`iceberg.enem_silver.participantes`).
- [ ] Adicionar testes de qualidade de dados e regressão para a harmonização.

---

## Etapa 4 — Agregações Analíticas e Machine Learning (Camada Gold)

### 4.1 Gold Analítica (`Spark SQL`)
- [ ] Calcular taxa de abstenção por ano, UF, dependência administrativa da escola, renda (`Q006`), raça/cor e sexo.
- [ ] Calcular estatísticas de desempenho (`CN`, `CH`, `LC`, `MT` e `Redação`) pelos mesmos recortes.
- [ ] Gravar as tabelas agregadas em formato **Apache Iceberg** (`iceberg.enem_gold.*`).

### 4.2 Modelo Preditivo de Risco de Abstenção (`Spark MLlib`)
- [ ] Selecionar apenas *features* anteriores à prova (perfil, escola, local e `Q001–Q025`), garantindo ausência de *data leakage* (sem notas ou status de redação).
- [ ] Realizar *split* temporal (treino em **2020–2022**, teste em **2023**).
- [ ] Treinar e comparar modelos de classificação binária (ex.: `LogisticRegression`, `RandomForestClassifier` / `GBTClassifier`).
- [ ] Avaliar métricas (AUC-ROC, F1-Score, Precision, Recall) e extrair a importância das variáveis (*Feature Importance*).
- [ ] Salvar métricas, importância das variáveis e resultados na camada Gold (`iceberg.enem_gold.ml_*`).

---

## Etapa 5 — Orquestração (Airflow) e Dashboard (Streamlit)
- [ ] Implementar a DAG ponta a ponta no `enem-airflow` (`Ingestão -> Bronze -> Silver -> Gold SQL & MLlib`) com *retries*, dependências e logs.
- [ ] Executar o pipeline completo nos dados reais (~6,88 GB / 16,58M registros).
- [ ] Construir painel interativo em **Streamlit** lendo a camada Gold para exibir evolução 2020–2023, desigualdades e fatores de risco de abstenção.

---

## Etapa 6 — Relatório Técnico (PDF) e Apresentação Final
- [ ] Escrever o **Relatório Técnico em PDF** contendo:
  - [ ] Introdução (contexto da fonte e problema resolvido + link do GitHub);
  - [ ] Descrição e caracterização da base (2020–2023);
  - [ ] Arquitetura da solução com diagrama e justificativa de cada ferramenta (incluindo o uso de Apache Iceberg com JDBC Catalog no lugar do Hive Metastore e a escolha contra HBase);
  - [ ] Explicação detalhada do pipeline e cuidados metodológicos;
  - [ ] Problemas encontrados e soluções adotadas;
  - [ ] Resultados obtidos (análise descritiva + métricas do modelo) e conclusões.
- [ ] Preparar apresentação de **10 a 15 minutos** para sala de aula.
- [ ] Consolidar entrega na branch `master` via Pull Request a partir de `develop`.

---

## Lembrete dos Critérios de Avaliação
- **Complexidade da solução:** 40%
- **Funcionamento do pipeline:** 20%
- **Qualidade da documentação:** 20%
- **Apresentação:** 20%
