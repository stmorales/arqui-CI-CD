# Pull base image
FROM python:3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock requirements.txt /code/
RUN pipenv install --system --dev
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000