from fastapi import HTTPException, status, APIRouter, Depends, Response
from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..database import get_db
from .. import oauth2, schemas, models, utils


router = APIRouter()


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect email or password')
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Incorrect email or password')
    access_token = oauth2.create_access_token(
        data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
