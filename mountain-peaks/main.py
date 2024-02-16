from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return "Welcome to Mountain Peaks application v0.1 - docker part"
