from dataclasses import dataclass
from datetime import datetime

@dataclass
class ConsumptionProfileDTO:
    NetWorkAreaName: str
    LPValue:int
    LPValueHL:int
    LPValueLL:int
    LPValueTot:int
    RegistrationTime:datetime
    Period:datetime

    @classmethod
    def from_dict(cls, data):
        return cls(
            NetWorkAreaName = data.get('NetWorkAreaName', None),
            LPValue = data.get('LPValue'),
            LPValueHL = data.get('LPValueHL', None),
            LPValueLL = data.get('LPValueLL', None),
            LPValueTot = data.get('LPValueTot', None),
            RegistrationTime = data.get('RegistrationTime'),
            Period = data.get('Period')
        )
    
