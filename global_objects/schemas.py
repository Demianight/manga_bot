from enum import StrEnum
from typing import Any
from pydantic import BaseModel, field_validator


class FormatSpecs(StrEnum):
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
        return (
            f'Название: {title_text}\n'
            f'Статус: {self.status}\n'
            f'Год написания: {self.year}\n'
            f'Последняя глава: {self.lastChapter if self.lastChapter else "Неизвестно"}\n'
        ).replace('None', 'Неизвестно')

    def __format__(self, format_spec: FormatSpecs) -> str:
        match format_spec:
            case FormatSpecs.SIMPLE:
                return str(self)
            case FormatSpecs.DETAILED:
                description_text = (
                    'Описание: ' + self.description['ru'] if 'ru' in self.description else self.description.get('en')
                )
                return str(self) + (description_text if description_text else 'Неизвестно')
