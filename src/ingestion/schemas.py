"""Pydantic schemas for IoT factory sensor data."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class SensorType(str, Enum):
    VIBRATION   = "vibration"
    TEMPERATURE = "temperature"
    PRESSURE    = "pressure"
    RPM         = "rpm"
    CURRENT     = "current"
    VOLTAGE     = "voltage"


class MachineType(str, Enum):
    PUMP        = "pump"
    COMPRESSOR  = "compressor"
    MOTOR       = "motor"
    CONVEYOR    = "conveyor"
    GEARBOX     = "gearbox"


class MachineMetadata(BaseModel):
    machine_id:    str
    machine_type:  MachineType
    location:      str
    manufacturer:  str
    model:         str
    install_date:  datetime
    criticality:   str = Field(default="medium", pattern=r"^(low|medium|high|critical)$")
    rated_rpm:     Optional[float] = None
    rated_power_kw:Optional[float] = None


class SensorReading(BaseModel):
    reading_id:   str
    machine_id:   str
    sensor_id:    str
    sensor_type:  SensorType
    value:        float
    unit:         str
    timestamp:    datetime
    quality:      float = Field(default=1.0, ge=0.0, le=1.0)
    raw_signal:   Optional[list[float]] = None   # For FFT processing

    @field_validator("value")
    @classmethod
    def value_is_finite(cls, v: float) -> float:
        import math
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Sensor value must be finite")
        return round(v, 6)

    @property
    def is_reliable(self) -> bool:
        return self.quality >= 0.7


class SensorBatch(BaseModel):
    machine_id: str
    timestamp:  datetime
    readings:   list[SensorReading]
    batch_id:   str

    @property
    def sensor_count(self) -> int:
        return len(self.readings)

    def to_kafka_dict(self) -> dict:
        return self.model_dump(mode="json")

# 15:09:53 — feat: implement machine pool with 50 simulated assets

# 15:09:53 — feat: add sensor calibration metadata to readings

# 14:16:38 — refactor: extract constant in schemas

# 14:19:31 — fix: handle None edge case in schemas

# 14:19:31 — fix: add missing type hint in schemas
