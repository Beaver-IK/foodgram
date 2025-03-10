# Стадия сборки зависимостей
FROM python:3.9-slim

WORKDIR /app

COPY requirements/requirements*.txt .

ARG ENV=prod

RUN python -m pip install --upgrade pip
    
RUN pip install -r requirements.${ENV}.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "foodgram.wsgi"]
