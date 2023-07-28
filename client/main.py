import asyncio
import random
import time
from string import Template
from string import ascii_letters, digits
from typing import TypedDict
from uuid import uuid4

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError


class RequestData(TypedDict):
    uuid: str
    text: str


def generate_string() -> str:
    card_symbols = f"{ascii_letters}{digits}"
    rand_code = ''.join(random.choice(card_symbols) for _ in range(16))
    return rand_code


async def generate_request_data() -> list[RequestData]:
    requests = list()
    for _ in range(random.randint(10, 100)):
        request_data = RequestData(uuid=str(uuid4()), text=generate_string())
        requests.append(request_data)
    return requests


class Client:

    def __init__(self):
        self._base_url = "http://server:8001"
        self._deleted_counter = 0
        self._time_start = time.perf_counter()

    async def add_data(self):
        while True:
            rout_url = "/api/v1/messages/"
            requests = await generate_request_data()
            try:
                async with aiohttp.ClientSession(self._base_url) as session:
                    for request in requests:
                        async with session.post(url=rout_url, json=request) as res:
                            await res.json()
                            await asyncio.sleep(0.9)
            except ClientConnectorError:
                continue

    async def get_data_with_count(self):
        while True:
            self.time_counter()
            requests = []
            get_rout_url = "/api/v1/messages/$counter/count/"
            try:
                async with aiohttp.ClientSession(self._base_url) as session:
                    rout_url_with_path_param = Template(get_rout_url).substitute(counter=10)
                    async with session.get(url=rout_url_with_path_param) as res:
                        requests += await res.json()

                        delete_rout_url = "/api/v1/messages/$uuid/"
                        for _ in range(len(requests)):
                            self.time_counter()
                            item_for_delete = requests.pop()
                            rout_url_with_path_param = Template(delete_rout_url).substitute(
                                uuid=item_for_delete.get("uuid"))
                            async with session.delete(url=rout_url_with_path_param):
                                self._deleted_counter += 1
                                await asyncio.sleep(1)
            except ClientConnectorError:
                continue

    def time_counter(self):
        e = time.perf_counter()
        if e - self._time_start >= 10:
            print(self._deleted_counter)
            self._time_start = e


async def main():
    client = Client()
    task_create = asyncio.create_task(client.add_data())
    task_get = asyncio.create_task(client.get_data_with_count())
    await asyncio.gather(task_create, task_get)


if __name__ == '__main__':
    asyncio.run(main())
