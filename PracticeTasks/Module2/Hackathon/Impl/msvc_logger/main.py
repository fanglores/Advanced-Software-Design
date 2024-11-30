import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:msvc_logger", host="127.0.0.1", port=8001, reload=True)
