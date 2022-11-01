# Pull base image
FROM python:3.8.5-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -q -r requirements.txt

COPY ./src /code

# EXPOSE 8000

# Run the app.  CMD is required to run on Heroku
CMD python /code/app.py
#CMD tail -f /dev/null