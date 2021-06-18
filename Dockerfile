FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip
COPY . .
CMD manage.py runserver 0:8000