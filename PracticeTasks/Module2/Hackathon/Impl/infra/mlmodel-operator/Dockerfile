FROM python:3.8-slim
WORKDIR /app
COPY operator.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["kopf", "run", "operator.py", "--verbose"]
