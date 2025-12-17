FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

ENV FLASK_ENV=production

CMD ["python", "app.py"]
