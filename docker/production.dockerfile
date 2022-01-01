FROM python:3.10-slim as build-image

RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/poetry
COPY pyproject.toml poetry.lock /root/poetry/

RUN pip install poetry --no-cache-dir \
    && poetry export --without-hashes > requirements.txt

ENV VENV_PATH=/opt/venv

RUN python -m venv $VENV_PATH \
    && . /opt/venv/bin/activate \
    && pip install -r requirements.txt --no-cache-dir


FROM python:3.10-slim as runtime-image

WORKDIR /app

COPY ./src/ /app/

ENV VENV_PATH=/opt/venv
COPY --from=build-image $VENV_PATH $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

CMD python main.py
