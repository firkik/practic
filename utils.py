from passlib.context import CryptContext

psw_contect = CryptContext(schemes=['bcrypt'])

def hash_password(password: str):
    return psw_contect.hash(password)

def verify_password(password, hashed_password):
    return psw_contect.verify(password, hashed_password)