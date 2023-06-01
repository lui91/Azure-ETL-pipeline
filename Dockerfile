# syntax=docker/dockerfile:1
FROM apache/airflow:2.5.1
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
COPY setup.py setup.py
RUN pip install -e .
USER 0
RUN apt-get update && apt-get install wget
COPY azure_cli_install.sh .
RUN chmod +x azure_cli_install.sh
RUN ./azure_cli_install.sh
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list
RUN apt update
RUN apt-get install terraform
USER 1