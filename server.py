from fastapi import FastAPI
from routers import file_ops

app = FastAPI()


@app.get('/')
async def init():
    return {"msg": "hello world!"}


app.include_router(file_ops.router)

# uvicorn server:app --host 127.0.0.1 --port 7777 --reload
