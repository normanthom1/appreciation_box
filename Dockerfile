FROM python:3.8-slim-buster
EXPOSE 8000
# Don't buffer Python logs (final crash will still get printed to log)

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt requirements.txt
# Install Python
RUN pip3 install -r requirements.txt

RUN PYTHONPATH=/app/usr/bin/python pip3 install -r requirements.txt
RUN PYTHONPATH=/app/usr/bin/python pip3 install gunicorn
COPY . /app
WORKDIR /app

#CMD ["python3", "manage.py", "migrate"]
CMD [ "gunicorn", "todo.wsgi:application", "--bind", "0.0.0.0:8000" ]


