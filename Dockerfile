# syntax=docker/dockerfile:1
FROM apache/airflow:2.5.1
COPY setup.py setup.py
RUN python setup.py install
COPY requirements.txt /
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt