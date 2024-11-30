from fastapi import FastAPI, HTTPException
from kubernetes import client, config
from model import ILogFile

msvc_logger = FastAPI(title="Logging Microservice", version="1.0.0", description="Fetch logs for pod in Kubernetes.")

@msvc_logger.get("/logs/{podName}", response_model=ILogFile, tags=["Logger"], summary="Fetch logs for a pod")
async def get_logs(podName: str):
    try:
        config.load_kube_config() # connect to cluster via kubeconfig file
        v1 = client.CoreV1Api()

        rawLogs = v1.read_namespaced_pod_log(name=podName, namespace="default")
        return ILogFile(podName=podName, logs=rawLogs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")