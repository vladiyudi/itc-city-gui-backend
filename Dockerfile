FROM python:3.8

RUN mkdir app

COPY . app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["python", "server.py"]
