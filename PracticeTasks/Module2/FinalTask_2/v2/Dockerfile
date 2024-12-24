# Dockerfile for serving either TF or scikit-learn model with FastAPI

FROM python:3.9-slim

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn gunicorn tensorflow scikit-learn joblib

# Copy the FastAPI app
COPY app.py /app/app.py

# We'll copy the model later in the Kaniko job, or download it at runtime
WORKDIR /app

# Expose port 80
EXPOSE 80

# Start server with Gunicorn + Uvicorn
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:80"]
