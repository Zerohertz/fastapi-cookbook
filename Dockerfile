FROM python:3.12-slim

LABEL maintainer="Zerohertz <ohg3417@gmail.com>"
LABEL description="Zerohertz's FastAPI Cookbook"
LABEL license="MIT"

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /workspace
COPY ./ /workspace

RUN apt-get update && \
    apt-get install make tzdata -y && \
    ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

RUN pip install uv==0.5.15 --no-cache-dir && \
    uv sync

ENTRYPOINT [ "make", "prod" ]
