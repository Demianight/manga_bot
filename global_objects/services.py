from httpx import AsyncClient, Response, HTTPStatusError, RemoteProtocolError
import asyncio
from io import BytesIO
import itertools
from pathlib import Path
from typing import Iterable

from aiolimiter import AsyncLimiter
from PIL import Image

from apps.errors.exceptions import RateLimitError
from env import settings
from global_objects.utils import normalize_filename

from .schemas import ChapterSchema, MangaSchema

from .variables import logger


class MangaService:
    def __init__(
            self,
            limiter: AsyncLimiter = AsyncLimiter(5, 1),
            base_url: str = "https://api.mangadex.org",
            image_base_url: str = "https://uploads.mangadex.org/data/",
            limit: int = 5
    ):
        self._base_url = base_url
        self._image_base_url = image_base_url
        self.default_timeout = 30
        self._client = AsyncClient(base_url=self._base_url, params={"limit": limit}, timeout=self.default_timeout)
        self._downloader = AsyncClient(base_url=f"{self._base_url}/at-home/server/", timeout=self.default_timeout)
        self._image_downloader = AsyncClient(base_url=self._image_base_url, timeout=self.default_timeout)
        self._limiter = limiter

    async def close(self):
        await self._client.aclose()
        await self._downloader.aclose()
        await self._image_downloader.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def get(
        self,
        url: str,
        client: AsyncClient | None = None,
        limiter: AsyncLimiter | None = None,
        retries: int = 3,
        delay: float = 1.0,
        **kwargs
    ) -> Response:
        client = client or self._client
        limiter = limiter or self._limiter

        attempt = 0
        while attempt < retries:
            async with limiter:
                try:
                    response = await client.get(url, **kwargs)
                    response.raise_for_status()
                    return response
                except RemoteProtocolError as e:
                    logger.error(f"RemoteProtocolError encountered on attempt {attempt + 1}: {e}")
                except HTTPStatusError as e:
                    logger.error(f"HTTP error occurred on attempt {attempt + 1}: {e}")
                    if response.status_code == 403:
                        raise RateLimitError
                except Exception as e:
                    logger.error(f"An unexpected error occurred on attempt {attempt + 1}: {e}")

            attempt += 1
            if attempt < retries:
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)

        # If we reach here, all retries have been exhausted
        raise Exception(f"Failed to fetch {url} after {retries} attempts")

    async def get_manga_by_id(self, manga_id: str) -> dict:
        response = await self.get(f"/manga/{manga_id}")
        return response.json()

    async def get_manga(self, title: str) -> list[MangaSchema]:
        response = await self.get("/manga", params={"title": title})
        data = response.json().get("data", [])
        return [MangaSchema.load_from_raw_response(raw) for raw in data]

    async def get_chapters(self, manga_id: str, offset: int = 0) -> list[ChapterSchema]:
        response = await self.get(
            "/chapter",
            params={
                "manga": manga_id,
                "translatedLanguage[]": ["ru"],
                "offset": offset,
            }
        )
        data = response.json().get("data", [])
        return [ChapterSchema.load_from_raw_response(raw) for raw in data]

    async def get_chapter_by_number(self, manga_id: str, chapter_num: int) -> ChapterSchema | None:
        response = await self.get(
            "/chapter",
            params={
                "manga": manga_id,
                "translatedLanguage[]": ["ru"],
                "chapter": chapter_num
            }
        )
        data = response.json().get("data", [])
        if not data:
            return None
        return ChapterSchema.load_from_raw_response(data[0])

    def _save_images_to_pdf(self, images: list[Image.Image], file_name: Path) -> Path:
        if images:
            images[0].save(file_name, save_all=True, append_images=images[1:])
        return file_name

    def _validate_file_name(self, file_name: str, default: str = 'no_name') -> Path:
        file_name = normalize_filename(file_name) or default
        file_path = settings.pdfs_folder / f'{file_name}.pdf'
        return file_path

    async def _get_images_from_urls(self, urls: list[str], hash: str) -> list[Image.Image]:
        tasks = [self.get(f'{hash}/{url}', self._image_downloader) for url in urls]
        responses = await asyncio.gather(*tasks)
        images = [Image.open(BytesIO(response.content)) for response in responses]
        return images

    async def download_chapter(self, chapter_id: str, file_name: str) -> Path:
        file_path = self._validate_file_name(file_name, chapter_id)
        if file_path.exists():
            return file_path

        response = await self.get(f"/{chapter_id}", client=self._downloader)
        data = response.json().get("chapter", {})
        urls = data.get('data', [])
        images = await self._get_images_from_urls(urls, data.get('hash', ''))
        return self._save_images_to_pdf(images, file_path)

    async def download_chapters(self, chapter_ids: Iterable[str], file_name: str) -> Path:
        file_path = self._validate_file_name(file_name)
        if file_path.exists():
            return file_path

        images = []
        tasks = []
        for chapter_id in chapter_ids:
            response = await self.get(f"/{chapter_id}", client=self._downloader)
            data = response.json().get("chapter", {})
            urls = data.get('data', [])
            tasks.append(self._get_images_from_urls(urls, data.get('hash', '')))
        images = list(itertools.chain.from_iterable(await asyncio.gather(*tasks)))
        return self._save_images_to_pdf(images, file_path)
