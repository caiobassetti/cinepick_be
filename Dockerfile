FROM python:3.10.6-buster

# First, pip install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Then only, install taxifare!
COPY api api
COPY keys keys
COPY raw_data raw_data

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
