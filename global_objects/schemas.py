from enum import StrEnum
from typing import Any

from pydantic import BaseModel, field_validator


class ChapterActions(StrEnum):
    SOLO = 'solo'
    RANGE = 'range'
    LIST = 'list'


class FormatOptions(StrEnum):
    SIMPLE = 'simple'
    DETAILED = 'detailed'


class MangaSchema(BaseModel):
    id: str
    title: dict[str, str]
    description: dict[str, str]
    status: str
    year: int | None
    lastChapter: str | None

    altTitles: dict[str, str] | Any

    @field_validator('altTitles')
    def normalize_alt_titles(cls, altTitles: list[dict[str, str]]):
        titles = {}
        for title in altTitles:
            for key, value in title.items():
                titles[key] = value

        return titles

    @classmethod
    def load_from_raw_response(cls, raw: dict[str, Any]):
        return MangaSchema(**raw['attributes'], id=raw["id"])

    def __str__(self):
        title_text = self.altTitles['ru'] if 'ru' in self.altTitles else self.altTitles.get('en')
        chapters_text = f"{self.lastChapter} (фактическое число может отличаться)" if self.lastChapter else "Неизвестно"
        return (
            f'Название: {title_text}\n'
            f'Статус: {self.status}\n'
            f'Год написания: {self.year}\n'
            f'Последняя глава: {chapters_text}\n'
        ).replace('None', 'Неизвестно')

    def __format__(self, format_spec: FormatOptions) -> str:
        match format_spec:
            case FormatOptions.SIMPLE:
                return str(self)
            case FormatOptions.DETAILED:
                description_text = (
                    'Описание: ' + self.description['ru'] if 'ru' in self.description else self.description.get('en')
                )
                return str(self) + (description_text if description_text else 'Неизвестно')


class ChapterSchema(BaseModel):
    id: str
    title: str
    chapter: float | int

    @field_validator('chapter')
    def normalize_chapter(cls, chapter: float):
        return int(chapter)

    @classmethod
    def load_from_raw_response(cls, raw: dict[str, Any]):
        return ChapterSchema(**raw['attributes'], id=raw["id"])

    def __str__(self):
        return (
            f'Глава: {int(self.chapter)}\n'
            f'Название: {self.title}\n'
        )

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case _:
                return str(self)
