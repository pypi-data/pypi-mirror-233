
import os
import time
import pathlib

from datetime import datetime

import urllib3

from .helper import MetalArchivesDirectory, ReleasePage, ReleasePages, normalize_keyword_casing


__FILE_DIRECTORY__ = pathlib.Path(__file__) \
                            .relative_to(os.getcwd()) \
                            .parent.resolve() \
                            .as_posix()


class HTTPSHandler:
    @staticmethod
    def get(url: str) -> dict:
        return urllib3.request('GET', url, timeout=urllib3.Timeout(read=None)).json()


class Releases:

    @staticmethod
    def get_upcoming(echo=0, page_size=100, wait=.1) -> list[ReleasePage]:
        data = ReleasePages()
        record_cursor = 0

        while True:
            endpoint = MetalArchivesDirectory.upcoming_releases(echo, record_cursor, page_size)
            response = HTTPSHandler.get(endpoint)
            releases = ReleasePage(**normalize_keyword_casing(response))

            data.append(releases)

            record_cursor += page_size
            echo += 1

            if releases.total_records - 1 > record_cursor:
                time.sleep(wait)
                continue
            break

        return data.combine()

    @staticmethod
    def get_all():
        raise NotImplementedError

    @staticmethod
    def get_range(range_start: datetime, range_stop: datetime, echo=0, page_size=100, wait=.1):
        data = ReleasePages()
        record_cursor = 0

        while True:
            endpoint = MetalArchivesDirectory.upcoming_releases(echo, record_cursor, page_size,
                                                                range_start.strftime('%Y-%m-%d'),
                                                                range_stop.strftime('%Y-%m-%d'))
            response = HTTPSHandler.get(endpoint)
            releases = ReleasePage(**normalize_keyword_casing(response))

            data.append(releases)

            record_cursor += page_size
            echo += 1

            if releases.total_records - 1 > record_cursor:
                time.sleep(wait)
                continue
            break

        return data.combine()
