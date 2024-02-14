FROM ubuntu:jammy

# Update the package list and install a sample package (e.g., curl)
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
    
RUN pip3 install -r requirements.txt

COPY ./app.py /app/app.py

EXPOSE 8501

CMD ["python3","app.py"]