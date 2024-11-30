from http.client import HTTPException
from fastapi import FastAPI


app = FastAPI()

@app.get("/what_path_should_be_here")
async def get_smth():
    try:
        return HTTPException(500, "Error")
    except:
        return HTTPException(500, "Error")