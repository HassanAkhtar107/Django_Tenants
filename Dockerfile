FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate_schemas --shared && python manage.py migrate_schemas --noinput && gunicorn DjangoProject.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]