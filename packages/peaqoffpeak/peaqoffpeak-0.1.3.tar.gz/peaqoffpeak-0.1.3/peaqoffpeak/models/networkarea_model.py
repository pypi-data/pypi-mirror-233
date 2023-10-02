from datetime import datetime
from dataclasses import dataclass, field
from .networkarea_dto import NetworkAreaDTO


@dataclass
class NetWorkAreaModel:
    displayname:str #show in dropdown
    networkareaid:str #use as networkareaid in call
    biddingarea:int #constraintareaid    
    isvalid: bool #isactive true and validto is null or future

    @classmethod
    def from_dto(cls, dto:NetworkAreaDTO):
        return cls(
            displayname = dto.NetworkArea,
            networkareaid = dto.NetworkAreaId,
            biddingarea = dto.ConstraintAreaId,
            isvalid = dto.IsActive and (dto.ValidTo is None or dto.ValidTo.lower == "null" or datetime.strptime(dto.ValidTo, "%Y-%m-%dT%H:%M:%S") > datetime.now())
        )
    