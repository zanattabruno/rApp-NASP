FROM python:3-slim-bullseye

RUN apt update && apt upgrade -y && apt autoremove -y

COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip && /usr/local/bin/python -m pip install -r requirements.txt

WORKDIR /app

COPY src/. /app/.

ENTRYPOINT ["sleep","999999999"]
