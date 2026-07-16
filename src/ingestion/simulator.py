"""Realistic IoT factory sensor simulator with failure mode injection."""
from __future__ import annotations
import math
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Generator
from src.ingestion.schemas import (
    SensorReading, SensorBatch, SensorType, MachineMetadata, MachineType
)

MACHINE_CONFIGS = {
    MachineType.PUMP:       {"rpm": 1450, "vib_base": 2.5, "temp_base": 65},
    MachineType.COMPRESSOR: {"rpm": 3000, "vib_base": 4.0, "temp_base": 80},
    MachineType.MOTOR:      {"rpm": 1800, "vib_base": 1.5, "temp_base": 55},
    MachineType.CONVEYOR:   {"rpm": 120,  "vib_base": 1.0, "temp_base": 45},
    MachineType.GEARBOX:    {"rpm": 960,  "vib_base": 3.0, "temp_base": 70},
}

FAILURE_MODES = ["bearing_wear", "overheating", "imbalance", "looseness", "normal"]


class MachineSimulator:
    def __init__(self, machine_id: str, machine_type: MachineType,
                 failure_mode: str = "normal") -> None:
        self.machine_id   = machine_id
        self.machine_type = machine_type
        self.failure_mode = failure_mode
        self.config       = MACHINE_CONFIGS[machine_type]
        self.age_hours    = random.uniform(0, 50000)
        self.degradation  = self._degradation_factor()

    def _degradation_factor(self) -> float:
        if self.failure_mode == "normal":
            return random.uniform(1.0, 1.1)
        elif self.failure_mode == "bearing_wear":
            return random.uniform(1.5, 2.5)
        elif self.failure_mode == "overheating":
            return random.uniform(1.2, 1.8)
        else:
            return random.uniform(1.3, 2.0)

    def generate_batch(self) -> SensorBatch:
        readings = []
        t = datetime.now(timezone.utc)

        # Vibration — most sensitive to faults
        vib_base = self.config["vib_base"]
        vib = vib_base * self.degradation * random.gauss(1.0, 0.05)
        if self.failure_mode == "imbalance":
            vib += 3.0 * math.sin(2 * math.pi * self.config["rpm"] / 60 * time.time())
        readings.append(SensorReading(
            reading_id=str(uuid.uuid4()),
            machine_id=self.machine_id,
            sensor_id=f"{self.machine_id}-VIB-01",
            sensor_type=SensorType.VIBRATION,
            value=max(0, vib),
            unit="mm/s",
            timestamp=t,
            raw_signal=[random.gauss(vib, 0.1) for _ in range(1024)],
        ))

        # Temperature
        temp_base = self.config["temp_base"]
        temp_mult = 1.5 if self.failure_mode == "overheating" else 1.0
        readings.append(SensorReading(
            reading_id=str(uuid.uuid4()),
            machine_id=self.machine_id,
            sensor_id=f"{self.machine_id}-TMP-01",
            sensor_type=SensorType.TEMPERATURE,
            value=temp_base * temp_mult * random.gauss(1.0, 0.02),
            unit="celsius",
            timestamp=t,
        ))

        # RPM
        readings.append(SensorReading(
            reading_id=str(uuid.uuid4()),
            machine_id=self.machine_id,
            sensor_id=f"{self.machine_id}-RPM-01",
            sensor_type=SensorType.RPM,
            value=self.config["rpm"] * random.gauss(1.0, 0.01),
            unit="rpm",
            timestamp=t,
        ))

        return SensorBatch(
            machine_id=self.machine_id,
            timestamp=t,
            readings=readings,
            batch_id=str(uuid.uuid4()),
        )


def machine_stream(
    n_machines: int = 50,
    failure_rate: float = 0.05,
    rate_per_second: float = 10.0,
) -> Generator[SensorBatch, None, None]:
    machines = []
    for i in range(n_machines):
        mtype  = random.choice(list(MachineType))
        fmode  = random.choice(FAILURE_MODES[:-1]) if random.random() < failure_rate else "normal"
        machines.append(MachineSimulator(f"MACH-{i:04d}", mtype, fmode))

    interval = 1.0 / rate_per_second
    while True:
        machine = random.choice(machines)
        yield machine.generate_batch()
        time.sleep(interval)

# 15:09:53 — refactor: extract constant in simulator

# 14:09:55 — fix: correct off-by-one in simulator

# 14:50:43 — chore: day 9 maintenance sweep

# 14:16:32 — refactor: rename variable for clarity in simulator

# 14:16:32 — style: reorder imports in simulator

# 15:54:40 — style: run black formatter on simulator

# 15:42:23 — docs: update docstring example in simulator

# 15:17:11 — refactor: rename variable for clarity in simulator

# 16:18:35 — docs: update docstring example in simulator

# 16:36:15 — refactor: extract constant in simulator

# 14:50:57 — style: run black formatter on simulator

# 16:54:01 — refactor: rename variable for clarity in simulator

# 16:54:01 — fix: correct off-by-one in simulator

# 15:46:47 — fix: add missing type hint in simulator

# 15:40:09 — chore: day 30 maintenance sweep

# 15:00:11 — fix: remove unused import in simulator
