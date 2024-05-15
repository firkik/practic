from database import Base
from sqlalchemy import Column ,String, Integer, Boolean, ForeignKey, TIMESTAMP, text

class Devide(Base):
    __tablename__ = 'device'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    system = Column(String, nullable=False)
    memory = Column(Integer, nullable=False)
    components = Column(Boolean, nullable=False)
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('current_time'))