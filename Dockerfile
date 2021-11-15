FROM python:3.7-alpine3.9
RUN apk update
RUN apk add gcc g++ make libffi-dev openssl-dev musl-dev 
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY crud /app/crud
COPY api.py /app
CMD ["python","api.py"]