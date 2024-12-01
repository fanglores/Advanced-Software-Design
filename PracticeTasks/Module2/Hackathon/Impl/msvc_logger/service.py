from fastapi import FastAPI, HTTPException, Depends, Request
from kubernetes import client, config
import httpx
import settings
from model import ILogFile

msvc_logger = FastAPI(title="Logging Microservice", version="1.0.0", description="Fetch logs for pod in Kubernetes.")
msvc_logger.mount(settings.path_base, msvc_logger)

async def authenticate_token(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        async with httpx.AsyncClient() as auth_client:
            response = await auth_client.post(f"{settings.url_base}/auth/validate", headers={"Authorization": auth_header})

            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Unauthorized")

        return True
    except:
        return False

@msvc_logger.get("/logs/{podName}", response_model=ILogFile, tags=["Logger"], summary="Fetch logs for a pod")
async def get_logs(podName: str, authorized: bool = Depends(authenticate_token, use_cache=True)):
    try:
        #TODO: Validate request by OpenAPI schema?
        if not authorized:
            raise HTTPException(status_code=401, detail="Unauthorized")

        #TODO: rework?
        config.load_kube_config() # connect to cluster via kubeconfig file
        v1 = client.CoreV1Api()

        rawLogs = v1.read_namespaced_pod_log(name=podName, namespace="default")
        return ILogFile(podName=podName, logs=rawLogs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")