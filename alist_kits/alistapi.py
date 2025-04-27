# coding:utf-8

"""
Reference: https://alist.nn.ci/zh/guide/api/
"""

from os.path import join
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from urllib.parse import urljoin

from xkits_lib import TimeUnit

from alist_kits.objects import MultiObject
from alist_kits.objects import SingleObject


def post_request(url: str, data: Dict[str, Any], timeout: TimeUnit = 15) -> Any:  # noqa:E501
    from requests import post  # pylint:disable=import-outside-toplevel

    (response := post(url, json=data, timeout=timeout)).raise_for_status()
    result: Dict[str, Any] = response.json()
    if result["code"] != 200 or result["message"] != "success":
        raise Warning(f"Invalid response: {result}")
    return result["data"]


class FS:  # pylint:disable=too-few-public-methods
    """https://alist.nn.ci/zh/guide/api/fs.html"""

    def __init__(self, base_url: str):
        self.__base_url = base_url

    @property
    def base(self) -> str:
        """base url"""
        return self.__base_url

    def search_with_list(self, keywords: str, parent: str = "/") -> Iterable[SingleObject]:  # noqa:E501
        """search with list api (when 403 Client Error occurs)"""
        objects: List[SingleObject] = []
        subdirs: List[SingleObject] = []
        for item in self.list(parent):
            if keywords in item["name"]:
                origin = item.origin
                origin.setdefault("parent", parent)
                objects.append(SingleObject(origin))
            if item["is_dir"]:
                subdirs.append(item)
        for item in subdirs:
            try:
                objects.extend(self.search_with_list(keywords, join(parent, item["name"])))  # noqa:E501
            except Warning:
                continue
        return objects

    def list(self, path: str = "/") -> MultiObject:
        url = urljoin(self.base, "/api/fs/list")
        data = {
            "path": path,
            "password": "",
            "page": 1,
            "per_page": 0,
            "refresh": False
        }
        return MultiObject(post_request(url, data))

    def get(self, path: str = "/") -> SingleObject:
        url = urljoin(self.base, "/api/fs/get")
        data = {
            "path": path,
            "password": "",
            "page": 1,
            "per_page": 0,
            "refresh": False
        }
        return SingleObject(post_request(url, data))
