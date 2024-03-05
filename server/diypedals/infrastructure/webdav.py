import datetime as dt
import http
import itertools
import xml.etree.ElementTree as ET
from base64 import b64encode
from typing import AsyncIterator

import httpx

from .. import settings
from ..domain.entities import BuildReport, Kit, Pcb, Photo
from .cache import DiskCache


class BuildReportClient:
    def __init__(self, username: str, password: str, cache: DiskCache) -> None:
        self._cache = cache
        self._http = httpx.AsyncClient(
            auth=httpx.BasicAuth(username, password),
            timeout=httpx.Timeout(5, connect=15),
        )

    async def fetch_all(self) -> AsyncIterator[BuildReport]:
        # https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/basic.html

        webdav_url = httpx.URL(settings.BUILD_REPORTS_WEBDAV_URL)

        ls_content = """<?xml version="1.0" encoding="UTF-8"?>
        <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
            <d:prop>
                <d:displayname/>
                <d:resourcetype/>
                <d:getlastmodified/>
            </d:prop>
        </d:propfind>
        """
        r = await self._http.request("PROPFIND", webdav_url, content=ls_content)

        xml = ET.fromstring(r.text)
        ns = {"d": "DAV:"}

        build_reports = []

        for item in itertools.islice(xml, 1, None):  # First is the folder itself
            if item.find(".//d:resourcetype/d:collection", ns) is None:
                continue

            href = item.find(".//d:href", ns)
            photos_url = webdav_url.copy_with(path=href.text + "entry.json")
            r = await self._http.request("GET", photos_url)
            r.raise_for_status()
            data = r.json()

            photos_url = webdav_url.copy_with(path=href.text + "photos")

            ls_photos_content = """<?xml version="1.0" encoding="UTF-8"?>
            <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
                <d:prop>
                    <d:displayname/>
                    <d:getcontenttype/>
                    <d:resourcetype/>
                    <d:getetag/>
                </d:prop>
            </d:propfind>
            """

            photos_response = await self._http.request(
                "PROPFIND", photos_url, content=ls_photos_content
            )

            photos = []

            if photos_response.status_code == http.HTTPStatus.MULTI_STATUS.value:
                photos_xml = ET.fromstring(photos_response.text)

                for photo_item in itertools.islice(photos_xml, 1, None):
                    if (
                        photo_item.find(".//d:resourcetype/d:collection", ns)
                        is not None
                    ):
                        continue

                    if not photo_item.find(".//d:getcontenttype", ns).text.startswith(
                        "image/"
                    ):
                        continue

                    async def _fetch_photo():
                        # Browser won't be able to download the image as it is behind authentication.
                        # Need to download the image and serve it as base64.
                        # See: https://stackoverflow.com/a/62305417
                        photo_url = webdav_url.copy_with(
                            path=photo_item.find(".//d:href", ns).text
                        )
                        photo_response = await self._http.request("GET", photo_url)
                        photo_content = photo_response.text

                        photo_src = "data:%s;base64,%s" % (
                            photo_response.headers["content-type"],
                            b64encode(photo_response.content).decode(),
                        )

                        return {"src": photo_src, "alt": "Photo"}

                    photo_etag = photo_item.find(".//d:getetag", ns).text
                    photo = Photo(**(await self._cache.get(photo_etag, _fetch_photo)))
                    photos.append(photo)

            yield BuildReport(
                title=data["title"],
                slug=data["slug"],
                description=data["description"],
                categories=data["categories"],
                build_date=dt.date.fromisoformat(data["build_date"]),
                status=data["status"],
                photos=photos,
                kit=Kit(**data.get("kit")) if data.get("kit") else None,
                pcb=Pcb(**data.get("pcb")) if data.get("pcb") else None,
            )
