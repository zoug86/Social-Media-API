from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project"}


@app.get("/posts")
def get_posts():
    return {"data": "Our Posts"}
