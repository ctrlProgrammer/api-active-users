FROM python:3.11.9-slim

WORKDIR /apps/active-users

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "./app.py", "--host:0.0.0.0"]