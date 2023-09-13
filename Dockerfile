FROM python:3.10-slim

RUN mkdir /dashapp
WORKDIR /dashapp

COPY ./ ./

RUN pip install -r ./requirements.txt

EXPOSE 8359

CMD ["gunicorn", "--workers=1", "--threads=1", "-b 0.0.0.0:8359", "main:server"]
