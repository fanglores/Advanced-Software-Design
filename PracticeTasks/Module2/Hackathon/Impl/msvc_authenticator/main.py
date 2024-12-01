import uvicorn
import settings

if __name__ == "__main__":
    uvicorn.run("main:msvc_authenticator", host="127.0.0.1", port=settings.msvc_authenticator_port, reload=True)
