from jose import JWSError, jwt
from datetime import datetime, timedelta, timezone
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = 'kl;sfdddddsdsdajfopooidsag'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
auth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')
        if id is None:
            raise credentials_exeption
        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credentials_exeption
    return token_data

def get_current_user(token: str = Depends(auth_scheme)):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
        )
    
    return verify_token(token, credentials_exeption)