FROM python:3.8

WORKDIR /src/app

COPY . .

RUN pip3 install -r requirements

CMD ["python3", "backup.py"]
