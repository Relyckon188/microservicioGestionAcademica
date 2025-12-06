FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV FLASK_CONTEXT=production
ENV FLASK_APP=app

RUN useradd --create-home --home-dir /home/sysacad sysacad
WORKDIR /home/sysacad

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chown -R sysacad:sysacad /home/sysacad
USER sysacad

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
