FROM python:3.5
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
WORKDIR /code/bjjtourneyfinder

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "bjjtourneyfinder.wsgi"]
