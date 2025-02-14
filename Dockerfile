FROM python:3-slim

COPY setup.py /setup.py
COPY api /api
COPY requirements.txt /requirements.txt
COPY test_data /test_data

RUN pip install --upgrade pip
RUN pip install -e .

CMD  uvicorn api.fast_api:app --host 0.0.0.0 --port $PORT
