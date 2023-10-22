# Используйте базовый образ Ubuntu
FROM python:3.11-slim

WORKDIR /app
#CREATE USER starlab WITH ENCRYPTED PASSWORD 'starlabpassword';
#GRANT ALL PRIVILEGES ON DATABASE starlabdatabase TO starlab;
# Установите необходимые пакеты и зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libmpc-dev \
    gcc \
    curl \
    postgresql \
    && python3 -m pip install --upgrade pip

# Установите зависимости Python из requirements.txt
COPY requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt

# Копируйте код приложения
COPY . /app/

# Установите переменную окружения PYTHONPATH
ENV PYTHONPATH=/app

# Добавьте метку
LABEL type="starlabTest"

# Запустите приложение
CMD ["python", "/app/app/main.py"]