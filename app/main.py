from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.params import Depends
# import psycopg2
# from psycopg2.extras import RealDictCursor
from sqlalchemy.orm.session import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI project"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING*",
    #                (new_post.title, new_post.content, new_post.published, id))
    # post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    updated_post.update(new_post.dict())
    db.commit()
    # db.refresh(updated_post)
    return updated_post.first()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id).delete()
    db.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {"post_deleted": "post deleted successfully"}

#### USER ####


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
