
import re

from datetime import datetime
from dataclasses import dataclass, field, InitVar


def normalize_keyword_casing(dictionary: dict):
    def normalize_to_snakecase(match: re.Match):
        preceding_text = match.group(1)
        text = match.group(2).lower()

        if preceding_text == '':
            return text

        return f'{preceding_text}_{text}'

    camel_case = re.compile(r'(\b|[a-z])([A-Z])')

    return {camel_case.sub(normalize_to_snakecase, k): v
            for k, v in dictionary.items()}


class MetalArchivesDirectory:

    @staticmethod
    def upcoming_releases(echo: int, display_start: int, display_length: 100,
                          from_date=datetime.now().strftime('%Y/%m/%d'), 
                          to_date='0000-00-00'):

        return (f'https://www.metal-archives.com/release/ajax-upcoming/json/1'
                f'?sEcho={echo}&iDisplayStart={display_start}&iDisplayLength={display_length}'
                f'&fromDate={from_date}&toDate={to_date}')


@dataclass
class BandLink:
    name: str = field(init=False)
    link: str = field(init=False)

    def __init__(self, band_link_html: str):
        ...


@dataclass
class AlbumLink:
    name: str = field(init=False)
    link: str = field(init=False)

    def __init__(self, album_link_html: str):
        ...


@dataclass
class Genres:
    full_genre: InitVar[str]

    def __post_init__(self, full_genre: str):
        ...


@dataclass
class AlbumRelease:
    band_link: InitVar[str]
    album_link: InitVar[str]
    release_type: InitVar[str]
    genres: InitVar[str]
    release_date: InitVar[str]
    added_date: InitVar[str]

    band: BandLink = field(init=False)
    album: AlbumLink = field(init=False)

    def __post_init__(self, band_link, album_link, *_):
        self.band = BandLink(band_link)
        self.album = AlbumLink(album_link)


@dataclass
class ReleasePage:
    total_records: int = field(init=False)
    total_display_records: int = field(init=False)
    echo: int = field(init=False)
    data: list[AlbumRelease] = field(init=False)

    def __init__(self, i_total_records: int, i_total_display_records: int,
                 s_echo: int, aa_data: list):

        self.total_records = i_total_records
        self.total_display_records = i_total_display_records
        self.echo = s_echo
        self.data = list(map(lambda n: AlbumRelease(*n), aa_data))

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('ReleasePage objects can only be summed '
                            'with other ReleasePage objects')

        self.data = self.data + other.data
        return self


class ReleasePages(list):
    def combine(self) -> ReleasePage:
        first_page, *remaining = self
        return sum(remaining, start=first_page)
