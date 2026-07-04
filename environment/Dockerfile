FROM python:3.13-slim-bookworm@sha256:18a6e328f4c744a72bab3f1d3c55ff0c01b97a8c71f4c1fd987d85f7d41e1e33

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log
