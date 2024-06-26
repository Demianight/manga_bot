from typing import Iterable, Sequence

from global_objects.schemas import ChapterActions, ChapterSchema
from global_objects import manga_service


def get_chapters_message(chapters: list[ChapterSchema]):
    header = 'Чтобы перейти на страницу с конкретной главой, просто отправь мне ее номер числом\n\n'
    chapters_text = '\n'.join([str(chapter) for chapter in chapters])
    return header + chapters_text


async def get_chapters_by_numbers(manga_id: str, numbers: Iterable[int]) -> tuple[list[ChapterSchema], list[int]]:
    errors = []
    chapters = []
    for number in numbers:
        chapter = await manga_service.get_chapter_by_number(manga_id, number)
        if not chapter:
            errors.append(number)
            continue
        chapters.append(chapter)
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
