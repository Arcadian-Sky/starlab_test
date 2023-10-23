FROM python:3.11-slim

# set work directory
WORKDIR /usr/src/app

# install dependencies first
COPY requirements.txt /usr/src/app
RUN apt-get update && apt-get install -y \
    build-essential \
    libmpc-dev \
    gcc \
    curl \
    postgresql \
    && python3 -m pip install --upgrade pip --no-cache-dir \
    && python3 -m pip install -r requirements.txt --no-cache-dir

# copy the app code
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app

LABEL type="starlabtest"

CMD ["python", "app/main.py"]