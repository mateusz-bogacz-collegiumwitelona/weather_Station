from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATEBASE_URL = "sqlite:///weather_data.db"

engine = create_engine(DATEBASE_URL, echo=False)

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<WeatherData(id={self.id}, timestamp={self.timestamp}, temperature={self.temperature}, humidity={self.humidity}, pressure={self.pressure})>"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()