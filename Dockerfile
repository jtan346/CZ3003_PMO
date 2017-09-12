FROM python:2.7

MAINTAINER andyccs

ADD ./requirements.txt /main/requirements.txt
WORKDIR /main
RUN pip install -r ./requirements.txt

ADD ./ /main
WORKDIR /main/src

EXPOSE 80

CMD ["python", "./manage.py", "runserver","--settings", "cmo.prod_settings", "0.0.0.0:80"]
