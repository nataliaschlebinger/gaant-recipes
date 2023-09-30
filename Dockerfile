FROM python:3.11

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
ENV PYTHONUNBUFFERED=1
RUN pip install -r requirements.txt

CMD ["python manage.py runserver 0.0.0.0:8000"]