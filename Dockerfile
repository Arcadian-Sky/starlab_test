FROM python:3.11-alpine

# set work directory
WORKDIR /usr/src/app

# install dependencies first
COPY requirements.txt /usr/src/app
RUN apk add --no-cache build-base \
    && apk add --no-cache mpc1-dev \
    && apk add --no-cache gcc curl \
    && apk add --no-cache postgresql \
    && python3 -m pip install --upgrade pip --no-cache-dir \
    && python3 -m pip install -r requirements.txt --no-cache-dir

# copy the app code
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app

LABEL type="starlabtest"

CMD ["python", "app/main.py"]