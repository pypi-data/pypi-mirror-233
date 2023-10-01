import aiohttp
import requests
from io import BytesIO
from prodia.exceptions import *

def request(method, url, api_key=None, body=None):
    headers = {'X-Prodia-Key': api_key, 'Content-Type': 'application/json'}
    r = requests.request(method, url, json=body, headers=headers)
    if r.status_code in [401, 402]:
        raise AuthorizationError(f"Prodia API returned {r.status_code}. Details: {r.text}")
    elif r.status_code == 400:
        raise InvalidParameter(f"Prodia API returned 400. Details: Invalid Generation Parameters")
    elif r.status_code not in [200, 400, 401, 402]:
        raise UnknownError(f"Prodia API returned {r.status_code}. Details: {r.text}")

    return r.json()

async def arequest(method, url, api_key=None, body=None):
    headers = {'X-Prodia-Key': api_key, 'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as s:
        async with s.request(method, url, json=body, headers=headers) as r:
            if r.status in [401, 402]:
                raise AuthorizationError(f"Prodia API returned {r.status}. Details: {await r.text()}")
            elif r.status == 400:
                raise InvalidParameter(f"Prodia API returned 400. Details: Invalid Generation Parameters")
            elif r.status not in [200, 400, 401, 402]:
                raise UnknownError(f"Prodia API returned {r.status}. Details: {await r.text()}")

            return await r.json()


def load(url):
    return BytesIO(requests.get(url).content)

async def aload(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return BytesIO(await response.read())