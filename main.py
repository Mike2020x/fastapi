from fastapi import FastAPI

app = FastAPI()


# get info
@app.get("/")
async def root():
    return "Hello FastAPI"


@app.get("/users")
async def get_user():
    return {"users": {}}
