# requirements-stage
FROM python:3.10-bullseye as requirements-stage

WORKDIR /tmp

# 설치 필요 패키지
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    openssl \
    wget \
    build-essential \
    vim

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && ln -s /opt/poetry/bin/poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /tmp/

# 종속성 설치
RUN poetry install --no-root

ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry export -f requirements.txt --output requirements.txt --dev --without-hashes; else poetry export -f requirements.txt --output requirements.txt --without-hashes; fi


FROM python:3.10-bullseye

# 설치 필요 패키지
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    openssl \
    wget \
    build-essential \
    vim

LABEL name="dhkim" version="0.1.0" description="Data Processing Application"

# 시간대 설정
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo "Asia/Seoul" > /etc/timezone
ENV TZ=Asia/Seoul

WORKDIR /src/

COPY --from=requirements-stage /tmp/requirements.txt /src/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

# 필요한 디렉토리 생성
RUN mkdir -p /src/crawl

COPY ./crawl /src/crawl/
COPY ./error_records_*.csv /src/
COPY ./stock_issue_dates.csv /src/stock_issue_dates.csv


CMD ["tail", "-f", "/dev/null"]
