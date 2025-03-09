FROM python:3.12.9-bookworm
ENV POETRY_VERSION=1.8.4
RUN pip install "poetry==$POETRY_VERSION"
# ENV PYTHONPATH="$PYTHONPATH:/app"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config installer.max-workers 10 && \
    poetry config virtualenvs.create false && \
    apt-get update && apt-get install -y g++ && \
    poetry install --no-interaction --no-root

COPY rock_spawner /app/rock_spawner

ENTRYPOINT sh start.sh