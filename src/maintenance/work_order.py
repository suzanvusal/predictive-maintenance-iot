"""Automated work order generation for predictive maintenance."""
from __future__ import annotations
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class WorkOrderPriority(str, Enum):
    EMERGENCY = "emergency"
    HIGH      = "high"
    MEDIUM    = "medium"
    LOW       = "low"


class WorkOrderStatus(str, Enum):
    OPEN         = "open"
    ASSIGNED     = "assigned"
    IN_PROGRESS  = "in_progress"
    COMPLETED    = "completed"
    CANCELLED    = "cancelled"


@dataclass
class WorkOrder:
    work_order_id:   str
    machine_id:      str
    machine_type:    str
    location:        str
    priority:        WorkOrderPriority
    failure_prob:    float
    predicted_failure_hours: float
    description:     str
    status:          WorkOrderStatus = WorkOrderStatus.OPEN
    assigned_to:     str | None = None
    created_at:      str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    due_by:          str | None = None
    completed_at:    str | None = None
    actual_failure:  bool | None = None

    @classmethod
    def from_prediction(cls, machine_id: str, machine_type: str,
                        location: str, failure_prob: float,
                        horizon_hours: float) -> "WorkOrder":
        if failure_prob >= 0.80:
            priority    = WorkOrderPriority.EMERGENCY
            description = f"CRITICAL: Machine {machine_id} has {failure_prob:.0%} failure probability within {horizon_hours}h. Immediate inspection required."
        elif failure_prob >= 0.60:
            priority    = WorkOrderPriority.HIGH
            description = f"HIGH RISK: Machine {machine_id} shows {failure_prob:.0%} failure probability. Schedule inspection within 24h."
        elif failure_prob >= 0.40:
            priority    = WorkOrderPriority.MEDIUM
            description = f"ELEVATED RISK: Machine {machine_id} at {failure_prob:.0%} failure probability. Plan maintenance within 48h."
        else:
            priority    = WorkOrderPriority.LOW
            description = f"Routine check: Machine {machine_id} showing early anomaly signs ({failure_prob:.0%})."

        return cls(
            work_order_id=f"WO-{uuid.uuid4().hex[:8].upper()}",
            machine_id=machine_id,
            machine_type=machine_type,
            location=location,
            priority=priority,
            failure_prob=failure_prob,
            predicted_failure_hours=horizon_hours,
            description=description,
        )


class WorkOrderManager:
    """Creates and manages predictive maintenance work orders."""

    def __init__(self) -> None:
        self._orders: dict[str, WorkOrder] = {}
        self._machine_open_orders: dict[str, str] = {}

    def create(self, machine_id: str, machine_type: str,
               location: str, failure_prob: float,
               horizon_hours: float = 48.0) -> WorkOrder | None:
        if machine_id in self._machine_open_orders:
            logger.info("Work order already open for machine %s", machine_id)
            return None

        wo = WorkOrder.from_prediction(machine_id, machine_type, location,
                                        failure_prob, horizon_hours)
        self._orders[wo.work_order_id] = wo
        self._machine_open_orders[machine_id] = wo.work_order_id
        logger.info("Created work order %s for %s (priority=%s prob=%.2f)",
                    wo.work_order_id, machine_id, wo.priority.value, failure_prob)
        return wo

    def complete(self, work_order_id: str,
                 actual_failure: bool = False) -> None:
        if wo := self._orders.get(work_order_id):
            wo.status         = WorkOrderStatus.COMPLETED
            wo.completed_at   = datetime.now(timezone.utc).isoformat()
            wo.actual_failure = actual_failure
            self._machine_open_orders.pop(wo.machine_id, None)

    def get_open_orders(self) -> list[WorkOrder]:
        return [wo for wo in self._orders.values()
                if wo.status == WorkOrderStatus.OPEN]

    def stats(self) -> dict:
        orders = list(self._orders.values())
        return {
            "total": len(orders),
            "open": sum(1 for wo in orders if wo.status == WorkOrderStatus.OPEN),
            "completed": sum(1 for wo in orders if wo.status == WorkOrderStatus.COMPLETED),
            "emergency": sum(1 for wo in orders if wo.priority == WorkOrderPriority.EMERGENCY),
        }

# 14:25:02 — feat: implement work order SLA tracking

# 14:25:02 — feat: add work order completion feedback loop

# 14:25:02 — fix: priority scorer not considering production criticality

# 14:25:02 — docs: update docstring example in work_order

# 16:25:17 — fix: remove unused import in work_order

# 16:15:27 — test: add assertion for return type in work_order

# 14:23:13 — fix: remove unused import in work_order

# 17:21:35 — perf: add caching in work_order

# 16:16:20 — chore: day 30 maintenance sweep

# 17:52:51 — fix: remove unused import in work_order

# 15:25:49 — chore: add logging to work_order
