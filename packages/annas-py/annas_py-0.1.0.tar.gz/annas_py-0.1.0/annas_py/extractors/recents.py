from html import unescape as html_unescape
from urllib.parse import urljoin

from requests import get

from ..models.data import RecentDownload
from . import BASE_URL


def get_recent_downloads() -> list[RecentDownload]:
    response = get(urljoin(BASE_URL, "dyn/recent_downloads"))
    data = response.json()
    return [
        RecentDownload(
            title=html_unescape(item["title"]), id=item["path"].split("/md5/")[-1]
        )
        for item in data
    ]
