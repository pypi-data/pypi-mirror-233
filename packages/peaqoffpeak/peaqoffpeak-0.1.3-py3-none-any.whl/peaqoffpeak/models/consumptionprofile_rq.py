from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class GetConsumptionProfileRq:        
    networkareaid:str = field(default=None)
    startdate:datetime = field(default=datetime.now() - timedelta(days=7))
    enddate:datetime = field(default=datetime.now())
    biddingarea:int = field(default=0)
    interval:int = field(default=0)
    
    def __post_init__(self):
        assert self.interval in [0,1] #0 = per dag, 1 = per månad
        assert self.biddingarea in [0,1,2,3,4] #elområden 1-4, 0 hela Sverige
        if self.networkareaid:
            self.networkareaid = self.networkareaid.upper()
        self.startdate = self.startdate.replace(hour=0, minute=0, second=0, microsecond=0)
        self.enddate = self.enddate.replace(hour=0, minute=0, second=0, microsecond=0)
