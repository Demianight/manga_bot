from httpx import AsyncClient

from apps.errors.exceptions import RequestException
from .schemas import MangaSchema


class MangaService:

    @property
    def client(self):
        return AsyncClient(base_url="https://api.mangadex.org", params={"limit": 5})

    async def get_manga_by_id(self, id):
        async with self.client as client:
            response = await client.get(f"/manga/{id}")
            if response.status_code != 200:
                raise RequestException
            return response

    async def get_manga(self, title: str) -> list[MangaSchema]:
        async with self.client as client:
            response = await client.get("/manga", params={"title": title})
            if response.status_code != 200:
                raise RequestException
            return [MangaSchema.load_from_raw_response(raw) for raw in response.json()["data"]]


manga_service = MangaService()
