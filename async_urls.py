from aiohttp import ClientSession
import requests
import asyncio
from typing import List, Dict, Any

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}


async def get_urls(url: str, session: ClientSession) -> list[str]:

    async with session.get(url) as response:
        data: Dict = await response.json()

        results: Dict = data.get("results")
        if results is None:
            return []
        image_urls: List[str] = [result.get("image") for result in results]

    return image_urls


async def main(urls: list) -> list[str]:
    async with ClientSession() as session:
        tasks: List[asyncio.Task] = []
        for url in urls:
            task: asyncio.Task = asyncio.create_task(get_urls(url, session))
            tasks.append(task)

        result: List[list] = await asyncio.gather(*tasks)

        all_image_urls: list[str] = []
        for image_url in result:
            all_image_urls.extend(image_url)

        return all_image_urls


base_url = "https://rickandmortyapi.com/api/character?page={}"
start_page = 1
end_page: int = (
    requests.get(base_url.format(start_page), headers=headers)
    .json()
    .get("info")
    .get("pages")
)
concrete_urls: list[str] = [
    base_url.format(page) for page in range(start_page, end_page + 1)
]
all_image_urls: list[str] = asyncio.run(main(urls=concrete_urls))


with open("urls.txt", "a") as f:
    for image_url in all_image_urls:
        f.write(image_url + "\n")
