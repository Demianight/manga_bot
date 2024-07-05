class MangaError(Exception):
    pass


class MangaDexAPIError(MangaError):
    pass


class RateLimitError(MangaDexAPIError):
    pass


class RequestError(MangaDexAPIError):
    pass
