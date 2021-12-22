FROM python:3.8.7-slim-buster

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV BACKEND_HOST="http://49.50.172.150"

RUN apt-get update && \
    pip install pip==21.2.4 && \
    pip install -r requirements.txt

CMD ["streamlit", "run", "front.py", "--server.port=8501"]
