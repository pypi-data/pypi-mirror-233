from __future__ import annotations

from requests.models import Response

from .souptools import (
    soup, soup_select, soup_select_one,
    xml, xml_select, xml_select_one,
)


class ResponseProxy(Response):
    def __init__(self, response):
        state = response.__reduce__()[2]
        self.__setstate__(state)  # type: ignore

    soup = soup
    soup_select = soup_select
    soup_select_one = soup_select_one
    xml = xml
    xml_select = xml_select
    xml_select_one = xml_select_one
