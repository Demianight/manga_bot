import asyncio
import os
from pathlib import Path
from typing import Sequence

from env import settings
from global_objects.schemas import ChapterActions, ChapterSchema
from global_objects import MangaService
from global_objects.variables import TO_MB, AnyPath


def get_chapters_message(chapters: list[ChapterSchema]):
    header = 'Чтобы перейти на страницу с конкретной главой, просто отправь мне ее номер числом\n\n'
    chapters_text = '\n'.join([str(chapter) for chapter in chapters])
    return header + chapters_text


async def get_chapters_by_numbers(manga_id: str, numbers: Sequence[int]) -> tuple[list[ChapterSchema], list[int]]:
    tasks = []
    async with MangaService() as manga_service:
        for number in numbers:
            tasks.append(manga_service.get_chapter_by_number(manga_id, number))
        chapters = await asyncio.gather(*tasks)
    errors = []
    for number, chapter in zip(numbers, chapters):
        if chapter is None:
            errors.append(number)
    chapters = [chapter for chapter in chapters if chapter]
    return chapters, errors


def define_action(text: str) -> ChapterActions | None:
    if ',' in text:
        return ChapterActions.LIST
    elif len(text.split('-')) == 2:
        return ChapterActions.RANGE
    elif text.isdigit():
        return ChapterActions.SOLO
    else:
        return None


def get_action_arguments(text: str, action: ChapterActions) -> Sequence[int]:
    match action:
        case ChapterActions.SOLO:
            return [int(text)]
        case ChapterActions.RANGE:
            start, end = text.split('-')
            return range(int(start), int(end) + 1)
        case ChapterActions.LIST:
            return list(map(int, text.split(',')))


def get_file_size_in_mb(file_path: AnyPath) -> float:
    return os.path.getsize(file_path) / TO_MB


def create_size_limit_message(file_size: float) -> str:
    return f'Файл слишком большой!\nРазмер: {file_size:.2f} МБ\n'
