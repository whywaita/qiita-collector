FROM python:3.6

MAINTAINER whywaita <https://github.com/whywaita>

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5000

ENTRYPOINT ["python", "manage.py"]
