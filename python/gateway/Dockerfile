FROM python:3.12-alpine

RUN apk add --no-cache bind-tools

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requeriments.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requeriments.txt

COPY . .

EXPOSE 8080

CMD ["python", "src/server.py"]