import os
import joblib
import tensorflow as tf
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

FRAMEWORK = os.environ.get("MODEL_FRAMEWORK", "sklearn")
MODEL_PATH = os.environ.get("MODEL_PATH", "/tmp/model")  # or any local path

model = None

@app.on_event("startup")
def load_model():
    global model
    if FRAMEWORK.lower() == "tensorflow":
        model = tf.keras.models.load_model(MODEL_PATH)
    else:
        # Assume scikit-learn
        model = joblib.load(MODEL_PATH)

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    # data is expected to be a JSON payload with features
    # This is a simple example - adapt as needed
    if FRAMEWORK.lower() == "tensorflow":
        # for TF, assume data is a list or array
        preds = model.predict(data["instances"]).tolist()
        return {"predictions": preds}
    else:
        # scikit-learn
        preds = model.predict(data["instances"]).tolist()
        return {"predictions": preds}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
