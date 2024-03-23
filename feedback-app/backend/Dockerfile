FROM ubuntu:jammy

# Update the package list and install a sample package (e.g., curl)
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt 

RUN pip3 install -r requirements.txt

COPY ./app.py /app/app.py
COPY ./templates/index.html /app/templates/index.html
COPY ./nginx.conf /etc/nginx/sites-available/default
COPY ./supervisord.conf /etc/supervisor/conf.d/
RUN touch gunicorn.log gunicorn.err

EXPOSE 8501

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]