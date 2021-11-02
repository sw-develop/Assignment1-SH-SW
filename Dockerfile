FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD    ./requirements.txt   /app/
RUN    pip install -r requirements.txt

ADD    ./assignment1   /app/assignment1/
ADD    ./gunicorn       /app/gunicorn/
ADD    ./manage.py      /app/

CMD ["gunicorn", "assignment1.wsgi", "-c", "gunicorn/prod.py"]
