

from datetime import datetime
from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    sensor_id: str = Field(..., example="virtual_001")
    co2: float = Field(..., example=420.5)
    pm25: float = Field(..., example=32.1)
    temp: float = Field(..., example=24.3)
    humidity: float = Field(..., example=55.8)
    timestamp: datetime | None = None


class SensorReadingWithML(SensorReading):
    is_anomaly: bool
    risk_level: int
    co2_next_pred: float


class StatusResponse(BaseModel):
    status: str
    total_readings: int
