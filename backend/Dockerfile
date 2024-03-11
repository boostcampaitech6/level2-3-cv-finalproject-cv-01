# backend/Dockerfile
# Stage 1 : Build
FROM python:3.10-slim as build

WORKDIR /workspace

# install required packages
RUN apt-get update \
	&& apt-get install -y --no-install-recommends git ssh gcc\
	&& rm -rf /var/lib/apt/lists/

# make github as a known host
RUN mkdir -p -m 0600 /root/.ssh \
	&& ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts

# COPY local SSH Key into Docker container
COPY id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

# install poetry settings
COPY pyproject.toml .
RUN pip install --upgrade pip \
    && pip install poetry \
	&& poetry export -f requirements.txt --output requirements.txt --without-hashes \
	&& git clone -b develop git@github.com:boostcampaitech6/level2-3-cv-finalproject-cv-01.git

# Stage 2 : Runtime
FROM python:3.10-slim as runtime

WORKDIR /workspace

# 필요한 파일들을 빌드 스테이지에서 복사
COPY --from=build /workspace/level2-3-cv-finalproject-cv-01 /workspace
COPY --from=build /workspace/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt \
	&& rm requirements.txt \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends git

CMD ["python", "backend/main.py"]