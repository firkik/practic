from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models as m
import schemas
import database
import utils
import token_1

router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(user_data: schemas.UserLogin, db = Depends(database.get_db)):
    user = db.query(m.User).filter(m.User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password'
        )
        
    if not utils.verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    access_token = token_1.create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}
    