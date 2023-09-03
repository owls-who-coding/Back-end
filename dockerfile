FROM python:3.10
WORKDIR /usr/scr/app

COPY requirements2.txt ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements2.txt

COPY . .

EXPOSE 8000

CMD ["python", "./server/manage.py", "runserver", "0.0.0.0:8000"]
