import uvicorn
import settings

if __name__ == "__main__":
    uvicorn.run("main:msvc_logger", host="127.0.0.1", port=settings.msvc_logger_port, reload=True)
