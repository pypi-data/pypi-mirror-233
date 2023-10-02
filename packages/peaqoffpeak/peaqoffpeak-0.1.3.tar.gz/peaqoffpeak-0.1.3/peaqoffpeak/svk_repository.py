from datetime import datetime
import json
import asyncio
import aiohttp
from models.networkarea_dto import NetworkAreaDTO
from models.consumptionprofile_dto import ConsumptionProfileDTO
from const import *
import logging

_LOGGER = logging.getLogger(__name__)

async def get_network_areas():
    ret = []
    try:
        data = await _call(uri='GetNetworkAreas')
        for d in data:
            inst = NetworkAreaDTO.from_dict(d)
            ret.append(inst)
    except Exception as e:
        _LOGGER.error(f"Error in getting Network areas from svk: {e}")
    return ret

async def get_consumption_profile(interval:int, startdate:datetime, enddate:datetime, biddingarea:int, networkareaid:str):
    params = {"interval":interval, "periodFrom":startdate.strftime("%Y-%m-%d"), "periodTo":enddate.strftime("%Y-%m-%d"), "biddingAreaId":biddingarea}
    if networkareaid:
        params["networkAreaId"] = networkareaid
    ret = []
    try:
        data = await _call(uri='GetConsumptionProfile', params=params)        
        for d in data:
            inst = ConsumptionProfileDTO.from_dict(d)
            ret.append(inst)
    except Exception as e:
        _LOGGER.error(f"Error in getting Consumption profile from svk: {e}")
    return ret
    

async def _call(uri, params=None):
    headers = {"Content-Type":"application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{ENDPOINT}{uri}", headers = headers, params=params) as response:
            try:
                return await response.json()                
            except Exception as e:
                raise Exception(f"Error in calling {uri}: {e}")



# if __name__ == "__main__":
#     ret = asyncio.run(get_network_areas())
#     for r in ret:
#         print(r)

# if __name__ == "__main__":
#     ret = asyncio.run(update_consumption_profile())
#     ttt = {v.Period: v.Value for v in ret}
#     print(ttt)
#     # for r in ret:
#     #     print(r)

