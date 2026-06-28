FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libxml2-dev libxslt1-dev libffi-dev libssl-dev sshpass ssh \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir ansible ncclient xmltodict paramiko

# Install required Ansible collections from provided requirements file
COPY ansible/requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install -r /tmp/requirements.yml || true

WORKDIR /workspace
COPY . /workspace

RUN chmod +x /workspace/entrypoint.sh

ENTRYPOINT ["/workspace/entrypoint.sh"]
