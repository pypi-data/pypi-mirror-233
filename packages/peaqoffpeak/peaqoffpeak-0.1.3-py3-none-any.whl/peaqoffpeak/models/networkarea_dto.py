from dataclasses import dataclass

@dataclass
class NetworkAreaDTO:
    NetworkArea: str
    NetworkAreaId: str
    NetworkAreaTypeName:str
    ConstraintAreaId:int
    ConstraintAreaName:str
    CompanyName:str
    EdielId:str
    IsActive:bool
    ValidFrom:str
    ValidTo:str
    BalanceProviders:str
    FutureBalanceProviders:str

    @classmethod
    def from_dict(cls, data):
        return cls(
            NetworkArea = data.get('NetworkArea'),
            NetworkAreaId = data.get('NetworkAreaId'),
            NetworkAreaTypeName = data.get('NetworkAreaTypeName'),
            ConstraintAreaId = data.get('ConstraintAreaId'),
            ConstraintAreaName = data.get('ConstraintAreaName'),
            CompanyName = data.get('CompanyName'),
            EdielId = data.get('EdielId'),
            IsActive = data.get('IsActive'),
            ValidFrom = data.get('ValidFrom'),
            ValidTo = data.get('ValidTo'),
            BalanceProviders = data.get('BalanceProviders'),
            FutureBalanceProviders = data.get('FutureBalanceProviders')
        )
    