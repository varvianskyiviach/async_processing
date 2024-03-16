from aiohttp import ClientSession
import asyncio
import os
from typing import List, Tuple

with open("urls.txt", "r") as file:
    all_image_urls: List[str] = file.readlines()


async def download_images(url: str, session: ClientSession) -> List[Tuple[bytes, str]]:
    async with session.get(url) as response:
        image_data: bytes = await response.read()

        return image_data, url


async def main(urls: list) -> List[Tuple[bytes, str]]:
    async with ClientSession() as session:

        tasks: list[asyncio.Task] = []
        for url in urls:
            url = url.replace("\n", "")
            task: asyncio.Task = asyncio.create_task(download_images(url, session))
            tasks.append(task)

        image_data_list: List[Tuple[bytes, str]] = await asyncio.gather(*tasks)

    return image_data_list


result = asyncio.run(main(all_image_urls))

if not os.path.exists("images"):
    os.makedirs("images")

for image_data, url in result:
    filename = url.split("/")[-1]
    with open(f"images/{filename}", "wb") as file:
        file.write(image_data)
