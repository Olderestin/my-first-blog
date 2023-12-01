FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /code/

RUN pip install --upgrade pip
RUN pip install -r code/requirements.txt
COPY . /code/
WORKDIR /code/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]