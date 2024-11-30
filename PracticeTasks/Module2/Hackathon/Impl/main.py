import uvicorn
from request_router import app
from fastapi import FastAPI

msvc_router = FastAPI()

msvc_router.mount("/what_path_should_be_here", app)

if __name__ == "__main__":
    uvicorn.run(msvc_router, host="127.0.0.1", port=8000, reload=True)
