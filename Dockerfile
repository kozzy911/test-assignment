# syntax=docker/dockerfile:1
FROM python:3.8.0

ADD ./certs/pypl2.crt /usr/local/share/ca-certificates/
ADD ./certs/combined_cacerts.pem /usr/local/etc/openssl/certs/

RUN mkdir -p /etc/ssl/certs/
RUN cat /usr/local/share/ca-certificates/pypl2.crt >> /etc/ssl/certs/ca-certificates.crt
RUN mkdir /root/.pip && echo "[global]" >> /root/.pip/pip.conf && echo "cert = /usr/local/share/ca-certificates/pypl2.crt" >> /root/.pip/pip.conf

RUN export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
RUN export SSL_CERT_FILE=/usr/local/etc/openssl/certs/combined_cacerts.pem

WORKDIR /code

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt update && apt -y install gcc libc-dev musl-dev postgresql python3-psycopg2
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "./reuters2.py"]
