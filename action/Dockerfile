FROM python:3.7

WORKDIR /app
COPY . /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
