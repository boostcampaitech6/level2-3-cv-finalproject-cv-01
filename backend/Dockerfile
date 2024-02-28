# backend/Dockerfile
FROM python:3.10

COPY . /workspace
WORKDIR /workspace
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]