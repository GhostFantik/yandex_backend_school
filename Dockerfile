FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN mkdir -p /code/
RUN mkdir -p /data/
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt