from dataclasses import dataclass
from datetime import datetime
from .consumptionprofile_dto import ConsumptionProfileDTO


@dataclass
class ConsumptionProfileModel:
    Period: datetime
    Value: int

    @classmethod
    def from_dto(cls, dto:ConsumptionProfileDTO):
        return cls(
            Period = datetime.strptime(dto.Period, "%Y-%m-%dT%H:%M:%S"),
            Value = dto.LPValue
        )