from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import urllib.parse
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Database connection setup
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
DATABASE = os.environ.get("MYSQL_DATABASE")
HOST = os.environ.get("MYSQL_HOST")
PASSWORD = urllib.parse.quote_plus(PASSWORD)
DATABASE_URL = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:3306/{DATABASE}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy model for SensorData
class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    unit = Column(String(10), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)


# Pydantic model for SensorData
class SensorDataModel(BaseModel):
    id: int
    sensor_id: int
    timestamp: datetime
    value: float
    lat: float
    lng: float
    unit: str
    type: str
    description: str

    class Config:
        orm_mode = True


# Initialize FastAPI application
app = FastAPI()


# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is up and running.
    """
    return "API is up and running. Query results or go to '/docs/' for documentation."


@app.get("/data/", response_model=List[SensorDataModel])
def read_data(skip: int = 0, limit: int = Query(default=100, le=1000), db: Session = Depends(get_db)):
    """
    Retrieve sensor data with pagination.
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    try:
        data = db.query(SensorData).offset(skip).limit(limit).all()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{sensor_id}", response_model=List[SensorDataModel])
def read_data_by_sensor(sensor_id: int, skip: int = 0, limit: int = Query(default=100, le=1000),
                        db: Session = Depends(get_db)):
    """
    Retrieve sensor data for a specific sensor with pagination.
    - **sensor_id**: ID of the sensor
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    try:
        data = db.query(SensorData).filter(SensorData.sensor_id == sensor_id).offset(skip).limit(limit).all()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/summary/", response_model=List[SensorDataModel])
def read_data_summary(
        type: Optional[str] = None,
        unit: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = Query(default=100, le=1000),
        db: Session = Depends(get_db)
):
    """
    Retrieve a summary of sensor data with optional filters.
    - **type**: Type of sensor data (e.g., temperature)
    - **unit**: Unit of measurement
    - **start_time**: Start time for the data query
    - **end_time**: End time for the data query
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    query = db.query(SensorData)

    if type:
        query = query.filter(SensorData.type == type)
    if unit:
        query = query.filter(SensorData.unit == unit)
    if start_time:
        query = query.filter(SensorData.timestamp >= start_time)
    if end_time:
        query = query.filter(SensorData.timestamp <= end_time)

    try:
        data = query.offset(skip).limit(limit).all()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/data/", response_model=SensorDataModel)
def create_sensor_data(sensor_data: SensorDataModel, db: Session = Depends(get_db)):
    """
    Create a new sensor data entry.
    - **sensor_data**: SensorDataModel containing the sensor data to be added
    """
    db_data = SensorData(**sensor_data.dict())
    try:
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/data/{data_id}", response_model=SensorDataModel)
def update_sensor_data(data_id: int, sensor_data: SensorDataModel, db: Session = Depends(get_db)):
    """
    Update an existing sensor data entry.
    - **data_id**: ID of the data entry to update
    - **sensor_data**: SensorDataModel containing the updated data
    """
    db_data = db.query(SensorData).filter(SensorData.id == data_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    for key, value in sensor_data.dict().items():
        setattr(db_data, key, value)

    try:
        db.commit()
        db.refresh(db_data)
        return db_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/data/{data_id}", response_model=SensorDataModel)
def delete_sensor_data(data_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing sensor data entry.
    - **data_id**: ID of the data entry to delete
    """
    db_data = db.query(SensorData).filter(SensorData.id == data_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    try:
        db.delete(db_data)
        db.commit()
        return db_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
