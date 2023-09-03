FROM python:3.10
WORKDIR /usr/scr/app

COPY server /usr/scr/app/server

WORKDIR /usr/scr/app/server

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000


# CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
CMD python ./manage.py runserver 0.0.0.0:8000
