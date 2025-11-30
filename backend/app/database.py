

from typing import List
from datetime import datetime

from .schemas import SensorReadingWithML

# armazenamento em memória
_MEASUREMENTS: List[SensorReadingWithML] = []


def save_measurement(measurement: SensorReadingWithML) -> None:
    """
    Persiste a leitura em memória.
    """
    if measurement.timestamp is None:
        measurement.timestamp = datetime.utcnow()
    _MEASUREMENTS.append(measurement)


def get_all_measurements() -> List[SensorReadingWithML]:
    return list(_MEASUREMENTS)


def get_latest_measurements(limit: int = 20) -> List[SensorReadingWithML]:
    return list(_MEASUREMENTS[-limit:])
