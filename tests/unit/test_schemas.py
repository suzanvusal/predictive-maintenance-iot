"""Unit tests for IoT sensor schemas."""
import uuid
import math
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from src.ingestion.schemas import SensorReading, SensorType, SensorBatch


def make_reading(**overrides) -> dict:
    base = dict(
        reading_id=str(uuid.uuid4()),
        machine_id="MACH-0001",
        sensor_id="MACH-0001-VIB-01",
        sensor_type=SensorType.VIBRATION,
        value=2.5,
        unit="mm/s",
        timestamp=datetime.now(timezone.utc),
    )
    base.update(overrides)
    return base


def test_valid_reading():
    r = SensorReading(**make_reading())
    assert r.value == 2.5

def test_value_rounded():
    r = SensorReading(**make_reading(value=2.123456789))
    assert r.value == 2.123457

def test_nan_value_rejected():
    with pytest.raises(ValidationError):
        SensorReading(**make_reading(value=float("nan")))

def test_inf_value_rejected():
    with pytest.raises(ValidationError):
        SensorReading(**make_reading(value=float("inf")))

def test_is_reliable_high_quality():
    r = SensorReading(**make_reading(quality=0.9))
    assert r.is_reliable

def test_is_reliable_low_quality():
    r = SensorReading(**make_reading(quality=0.5))
    assert not r.is_reliable

def test_sensor_batch_count():
    readings = [SensorReading(**make_reading(sensor_id=f"S-{i}")) for i in range(3)]
    batch = SensorBatch(
        machine_id="MACH-0001",
        timestamp=datetime.now(timezone.utc),
        readings=readings,
        batch_id=str(uuid.uuid4()),
    )
    assert batch.sensor_count == 3

# 15:09:53 — feat: add failure mode injection in simulator (bearing wear,
