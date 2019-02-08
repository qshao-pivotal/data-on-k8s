FROM python:3.6.8
COPY requirements.txt indexer.py /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD python indexer.py