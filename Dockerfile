FROM python:3.10-slim

WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

ADD pd.py /app/

ENTRYPOINT ["python", "/app/pd.py"]