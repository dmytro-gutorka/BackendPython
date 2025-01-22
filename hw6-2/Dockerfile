FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD ["python3", "-m", "app.run"]

