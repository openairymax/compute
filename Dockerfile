# SPDX-License-Identifier: Apache-2.0
#
# amax 命令行容器镜像。amax 仅依赖 Python 标准库，
# 单阶段构建即可；安装后清理源码目录，镜像里只留
# site-packages 与 console script。

FROM python:3.12-slim

LABEL org.opencontainers.image.title="amax" \
      org.opencontainers.image.description="AMAX (AirymaxCompute) — the job & receipt layer of the Airymax stack" \
      org.opencontainers.image.source="https://atomgit.com/openairymax/compute" \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.vendor="OpenAirymax"

WORKDIR /src
COPY pyproject.toml ./
COPY amax/ ./amax/
RUN pip install --no-cache-dir . && rm -rf /src

RUN amax --version

ENTRYPOINT ["amax"]
