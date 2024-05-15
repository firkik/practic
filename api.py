from schemas import DeviceScheme, UpdateDeviceScheme, UserCreate, UserLogin, UserOut
from database import engine, get_db, Session
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException, Response, status
import utils
import models as m
import uvicorn
import auth
import token_1

api = FastAPI(debug=True, check_same_thread=False)
m.Base.metadata.create_all(bind=engine)
psw_contect = CryptContext(schemes=['bcrypt'])


# Работа с пользователем

api.include_router(auth.router)

@api.get('/users')
async def read_users(db = Depends(get_db)):
    users = db.query(m.User).all()
    return users

@api.post('/users', status_code=status.HTTP_201_CREATED)
async def create_users(user: UserCreate, db = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = m.User(**user.model_dump())
    db.add(new_user)
    db.commit()   # Сохраняет информацию
    db.refresh(new_user)  # Выставляет id для записи
    return {'messages': 'Пользователь успешно зарегистрирован!', 'data': new_user}


# Основной API


@api.get('/devices')
async def get_devices_all(db = Depends(get_db), get_current_user: int = Depends(token_1.get_current_user) ):
    devices = db.query(m.Devide).all()
    return devices

@api.get('/device/{id}')
async def get_device_one(id: int, db = Depends(get_db), get_current_user: int = Depends(token_1.get_current_user) ):
    device = db.query(m.Devide).filter(m.Devide.id == id).first()
    return device

@api.post('/device')
async def app_device(device_component: DeviceScheme, db = Depends(get_db), get_current_user: int = Depends(token_1.get_current_user) ):
    new_device = m.Devide(**device_component.model_dump())
    db.add(new_device)
    db.commit()   # Сохраняет информацию
    db.refresh(new_device)  # Выставляет id для записи
    return {'message': 'Данные были успешно добавлены!', 'data': device_component}

@api.put('/device/{id}')
async def update_device(id: int, device_component: UpdateDeviceScheme, db = Depends(get_db), get_current_user: int = Depends(token_1.get_current_user) ):
    device = db.query(m.Devide).filter(m.Devide.id == id)
    device.update(device_component.model_dump())
    db.commit()
    return {'message': 'Данные были успешно изменены!', 'data': device_component}

@api.delete('/device/{id}')
async def delete_device(id: int, db = Depends(get_db), get_current_user: int = Depends(token_1.get_current_user) ):
    device = db.query(m.Devide).filter(m.Devide.id == id).first()
    db.delete(device)
    db.commit()
    return {'message': 'Данные были успешно удалены!', 'data': device}


if __name__ ==  '__main__':
    try:
        uvicorn.run(api, port=8888)
    except KeyboardInterrupt:
        print('\n...Закрытие программы.\n')