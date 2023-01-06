FROM python:3.8-slim-buster
EXPOSE 8000

# ENV http_proxy="http://10.174.8.26:3128"
# ENV https_proxy="http://10.174.8.26:3128"
# # ARG http_proxy
# ARG https_proxy

# Don't buffer Python logs (final crash will still get printed to log)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

#required for postgres
#RUN apt update --allow-releaseinfo-change --no-cache && apt upgrade -y  \
#    && apt install -y build-essential \
#    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
RUN PYTHONPATH=/usr/bin/python pip3 install -r requirements.txt
COPY . .
CMD ["python3", "manage.py", "makemigrations"]
CMD ["python3", "manage.py", "migrate"]
#CMD ['python3', 'manage.py', 'runserver', '0.0.0.0:8004']

