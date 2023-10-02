from datetime import datetime
import svk_repository as repo
from models.consumptionprofile_model import ConsumptionProfileModel
from models.networkarea_model import NetWorkAreaModel
from models.consumptionprofile_rq import GetConsumptionProfileRq


# class SvkCache:
#     """Cache for SVK API"""
#     VALIDITY_AREAS = 60 * 60 * 24 #24 hours
#     VALIDITY_CONSUMPTION_PROFILE = 60 * 60 #1 hour
    
#     def __init__(self):
#         self.network_areas = {}
#         self.consumption_profiles = {}

#     def invalidate(self) -> None:
#         self.network_areas = {}
#         self.consumption_profiles = {}

#     def get_network_areas(self) -> list[NetWorkAreaModel]:
#         if not self.network_areas:
#             return None
#         if self.network_areas.keys[0] + self.VALIDITY_AREAS < datetime.now().timestamp():
#             return None
#         return self.network_areas


async def get_network_areas() -> list[NetWorkAreaModel]:
    """Get all network areas from SVK API"""
    dto = await repo.get_network_areas()
    ret = []
    for d in dto:
        inst = NetWorkAreaModel.from_dto(d)
        ret.append(inst)
    return ret


async def check_network_area_valid(networkareaid:str) -> bool:
    """Check if network area is valid"""
    all_areas = await get_network_areas()
    return networkareaid in [a.networkareaid for a in all_areas if a.isvalid]


async def get_consumption_profile(request: GetConsumptionProfileRq) -> list[ConsumptionProfileModel]:
    """Get consumption profile from SVK API"""
    _enddate = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dto = await repo.get_consumption_profile(
        interval=request.interval, 
        startdate=request.startdate, 
        enddate=request.enddate, 
        biddingarea=request.biddingarea, 
        networkareaid=request.networkareaid)    
    ret = []    
    for d in dto:
        inst = ConsumptionProfileModel.from_dto(d)
        if inst.Period.date() < _enddate.date():
            ret.append(inst)
    return ret


import asyncio

if __name__ == "__main__":
    # ret = asyncio.run(get_network_areas())
    # for r in ret:
    #     print(r)

    request = GetConsumptionProfileRq()
    #print(request)
    ret = asyncio.run(get_consumption_profile(request))
    for r in ret:
        print(r)