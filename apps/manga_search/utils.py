from global_objects.schemas import ChapterSchema


def get_chapters_message(chapters: list[ChapterSchema]):
    header = 'Чтобы перейти на страницу с конкретной главой, просто отправь мне ее номер числом\n\n'
    chapters_text = '\n'.join([str(chapter) for chapter in chapters])
    return header + chapters_text
