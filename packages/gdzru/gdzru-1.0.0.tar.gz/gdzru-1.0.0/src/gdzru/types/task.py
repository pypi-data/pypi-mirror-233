#                © Copyright 2023
#         Licensed under the MIT License
#       https://opensource.org/licenses/MIT
#    https://github.com/Den4ikSuperOstryyPer4ik

from gdzru.types.type import Type


class Paths(Type):
    action: str | None = None
    controller: str | None = None


class Cover(Type):
    title: str | None = None
    url: str | None = None


class Price(Type):
    purchase: int | None = None
    download: int | None = None


class Book(Type):
    id: int | None = None
    parent_id: int | None = None
    country: str | None = None
    subject_id: int | None = None
    title: str | None = None
    header: str | None = None
    breadcrumb: str | None = None
    year: str | None = None
    classes: list[int] | None = None
    authors: list[str] | None = None
    authors_ru: list | None = None
    authors_en: list | None = None
    authors_by: list | None = None
    authors_ua: list | None = None
    description: str | None = None
    publisher: str | None = None
    category: str | None = None
    series: str | None = None
    subtype: str | None = None
    study_level: str | None = None
    parts: list[str] | None = None
    cover: Cover | None = None
    cover_url: str | None = None
    search_keywords: str | None = None
    price: Price | None = None
    tasks_view: str | None = None
    is_paid: bool | None = None
    url: str | None = None
    priority: int | None = None
    updated_at: int | None = None


class Task(Type):
    title: str | None = None
    title_short: str | None = None
    description: str | None = None
    youtube_video_id: str | None = None
    url: str | None = None


class Image(Type):
    title: str | None = None
    url: str | None = None


class Edition(Type):
    title: str | None = None
    description: str | None = None
    type: int | None = None
    publisher_id: int | None = None
    texts: list | None = None
    images: list[Image] | None = None
    youtube_videos: list | None = None


class PaidContent(Type):
    watched: int | None = None
    limit: int | None = None
    tasks: list | None = None


class TaskInfo(Type):
    success: bool | None = None
    message: str | None = None
    paths: Paths | None = None
    book: Book | None = None
    task: Task | None = None
    editions: list[Edition] | None = None
    paid_content: PaidContent | None = None
