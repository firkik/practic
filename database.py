from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


DATABASE_URL = 'sqlite:///device.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

def get_db():
    try:
        database = Session()
        yield database
    except:
        print('Произошла ошибка сервера...')
    finally:
        database.close()
    