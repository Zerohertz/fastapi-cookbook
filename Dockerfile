FROM python:3.12-slim

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Zerohertz's FastAPI Boilerplate"
LABEL license="MIT"

WORKDIR /workspace
COPY ./ /workspace

RUN apt-get update && apt-get install make -y

RUN pip install uv==0.5.15 --no-cache-dir && \
    uv sync

ENTRYPOINT [ "make", "prod" ]
