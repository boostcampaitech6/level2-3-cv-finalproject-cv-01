# backend/Dockerfile
# Stage 1 : Build
FROM python:3.10-slim as build

COPY . /workspace
WORKDIR /workspace

# install required packages
RUN apt-get update \
	&& apt-get install -y --no-install-recommends git \
	&& apt-get install -y --no-install-recommends ssh \
	&& apt-get install -y gcc \
	&& rm -rf /var/lib/apt/lists/

# install poetry settings
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2 : Runtime
FROM python:3.10-slim as runtime

WORKDIR /workspace
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# 필요한 파일들을 빌드 스테이지에서 복사
COPY --from=build /workspace /workspace
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]