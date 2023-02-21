# syntax=docker/dockerfile:1
FROM apache/airflow:2.5.1
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
COPY setup.py setup.py
RUN pip install -e .
USER 0
COPY install-az.sh .
RUN ./install-az.sh
USER 1