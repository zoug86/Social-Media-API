from fastapi import FastAPI
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router, tags=["Posts"])
app.include_router(user.router, tags=["Users"])
app.include_router(auth.router,  tags=["Authentication"])


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project"}


# Connect to an existing database
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='fastapi', user='postgres', password='123123h', port=5432, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected to database!")
#         break
#     except (Exception, psycopg2.Error) as error:
#         print("Unable to connect to the database!")
#         print("Error: ", error)
#         time.sleep(2)
