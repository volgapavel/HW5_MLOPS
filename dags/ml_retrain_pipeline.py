# dags/ml_retrain_pipeline.py

import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")


def train_model():
    print("Модель обучена")


def evaluate_model():
    print("Модель оценена, метрики в норме")


def deploy_model():
    print("Модель выведена в продакшен")


with DAG(
    dag_id="ml_retrain_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "retrain"]
) as dag:

    train = PythonOperator(task_id="train_model", python_callable=train_model)
    evaluate = PythonOperator(task_id="evaluate_model", python_callable=evaluate_model)
    deploy = PythonOperator(task_id="deploy_model", python_callable=deploy_model)

    notify = EmailOperator(
        task_id="notify_success",
        to="volgapavel@gmail.com",
        subject="Новая модель в продакшене",
        html_content=f"Новая модель <b>{MODEL_VERSION}</b> успешно развернута"
    )

    train >> evaluate >> deploy >> notify

