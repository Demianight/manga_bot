import asyncio
from io import BytesIO
from PIL import Image
from httpx import AsyncClient

from apps.errors.exceptions import RequestException
from .schemas import ChapterSchema, MangaSchema


class MangaService:

    @property
    def client(self):
        return AsyncClient(
            base_url="https://api.mangadex.org",
            params={"limit": 5}
        )

    @property
    def downloader(self):
        return AsyncClient(
            base_url="https://api.mangadex.org/at-home/server/",
        )

    @property
    def image_downloader(self):
        return AsyncClient(
            base_url="https://uploads.mangadex.org/data/",
        )

    async def get_manga_by_id(self, id):
        async with self.client as client:
            response = await client.get(f"/manga/{id}")
            if response.status_code != 200:
                raise RequestException
            return response

    async def get_manga(self, title: str) -> list[MangaSchema]:
        async with self.client as client:
            response = await client.get(
                "/manga",
                params={"title": title}
            )
            try:
                data = response.json()["data"]
                return [MangaSchema.load_from_raw_response(raw) for raw in data]
            except KeyError:
                raise RequestException(response.text)

    async def get_chapters(self, manga_id: str, offset: int = 0) -> list[ChapterSchema]:
        async with self.client as client:
            response = await client.get(
                "/chapter",
                params={
                    "manga": manga_id,
                    "translatedLanguage[]": ["ru"],
                    "offset": offset,
                },
            )
            try:
                data = response.json()["data"]
                return [ChapterSchema.load_from_raw_response(raw) for raw in data]
            except KeyError:
                raise RequestException(response.text)

    def save_images_to_pdf(self, images: list[Image.Image], file_name: str):
        if images:
            images[0].save(file_name, save_all=True, append_images=images[1:])
        return file_name

    async def get_images_from_urls(self, urls: list[str], hash: str) -> list[Image.Image]:
        async with self.image_downloader as client:
            tasks = [client.get(f'{hash}/{url}') for url in urls]
            responses = await asyncio.gather(*tasks)
            images = [Image.open(BytesIO(response.content)) for response in responses]
            return images

    async def download_chapter(self, chapter_id: str):
        async with self.downloader as client:
            response = await client.get(f"/{chapter_id}")
            try:
                data = response.json()["chapter"]
                urls = data['data']
                images = await self.get_images_from_urls(urls, data['hash'])
                return self.save_images_to_pdf(images, f'pdfs/{chapter_id}.pdf')
            except KeyError:
                raise RequestException(response.text)


manga_service = MangaService()
