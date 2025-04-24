# coding:utf-8

import unittest
from unittest import mock

from alist_kits.alistapi import FS
from alist_kits.alistapi import post_request
from alist_kits.objects import MultiObject
from alist_kits.objects import SingleObject


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url: str = "https://example.com/"

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("requests.post")
    def test_post_code_error(self, mock_post):
        fake_data = {
            "code": 500,
            "message": "success",
            "data": None
        }
        fake_post = mock.MagicMock()
        fake_post.json.side_effect = [fake_data]
        mock_post.side_effect = [fake_post]
        self.assertRaises(Warning, post_request, self.base_url, {})

    @mock.patch("requests.post")
    def test_post_message_error(self, mock_post):
        fake_data = {
            "code": 200,
            "message": "Object not found",
            "data": None
        }
        fake_post = mock.MagicMock()
        fake_post.json.side_effect = [fake_data]
        mock_post.side_effect = [fake_post]
        self.assertRaises(Warning, post_request, self.base_url, {})


class TestFS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url: str = "https://example.com/"
        cls.fs = FS(cls.base_url)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("requests.post")
    def test_list(self, mock_post):
        fake_data = {
            "code": 200,
            "message": "success",
            "data": {
                "content": [
                    {
                        "name": "Alist V3.md",
                        "size": 1592,
                        "is_dir": False,
                        "modified": "2024-05-17T13:47:55.4174917+08:00",
                        "created": "2024-05-17T13:47:47.5725906+08:00",
                        "sign": "",
                        "thumb": "",
                        "type": 4,
                        "hashinfo": "null",
                        "hash_info": None
                    }
                ],
                "total": 1,
                "readme": "",
                "header": "",
                "write": True,
                "provider": "Local"
            }
        }
        fake_post = mock.MagicMock()
        fake_post.json.side_effect = [fake_data]
        mock_post.side_effect = [fake_post]
        self.assertIsInstance(object := self.fs.list(), MultiObject)
        self.assertEqual(object.origin, fake_data["data"])
        self.assertEqual(len(object), object.origin["total"])
        self.assertEqual(object["content"], fake_data["data"]["content"])
        self.assertEqual(object["readme"], "")
        self.assertEqual(object["header"], "")
        self.assertEqual(object["write"], True)
        self.assertEqual(object["provider"], "Local")
        for item in object:
            self.assertIsInstance(item, SingleObject)
            self.assertEqual(item.origin, fake_data["data"]["content"][0])
            self.assertEqual(item["name"], "Alist V3.md")
            self.assertEqual(item["size"], 1592)
            self.assertEqual(item["is_dir"], False)
            self.assertEqual(item["modified"], "2024-05-17T13:47:55.4174917+08:00")  # noqa:E501
            self.assertEqual(item["created"], "2024-05-17T13:47:47.5725906+08:00")  # noqa:E501
            self.assertEqual(item["sign"], "")
            self.assertEqual(item["thumb"], "")
            self.assertEqual(item["type"], 4)
            self.assertEqual(item["hashinfo"], "null")
            self.assertEqual(item["hash_info"], None)

    @mock.patch("requests.post")
    def test_get(self, mock_post):
        fake_data = {
            "code": 200,
            "message": "success",
            "data": {
                "name": "Alist V3.md",
                "size": 2618,
                "is_dir": False,
                "modified": "2024-05-17T16:05:36.4651534+08:00",
                "created": "2024-05-17T16:05:29.2001008+08:00",
                "sign": "",
                "thumb": "",
                "type": 4,
                "hashinfo": "null",
                "hash_info": None,
                "raw_url": "http://127.0.0.1:5244/p/local/Alist%20V3.md",
                "readme": "",
                "header": "",
                "provider": "Local",
                "related": None
            }
        }
        fake_post = mock.MagicMock()
        fake_post.json.side_effect = [fake_data]
        mock_post.side_effect = [fake_post]
        self.assertIsInstance(object := self.fs.get(), SingleObject)
        self.assertEqual(object.origin, fake_data["data"])
        self.assertEqual(object["name"], "Alist V3.md")
        self.assertEqual(object["size"], 2618)
        self.assertEqual(object["is_dir"], False)
        self.assertEqual(object["modified"], "2024-05-17T16:05:36.4651534+08:00")  # noqa:E501
        self.assertEqual(object["created"], "2024-05-17T16:05:29.2001008+08:00")  # noqa:E501
        self.assertEqual(object["sign"], "")
        self.assertEqual(object["thumb"], "")
        self.assertEqual(object["type"], 4)
        self.assertEqual(object["hashinfo"], "null")
        self.assertEqual(object["hash_info"], None)
        self.assertEqual(object["raw_url"], "http://127.0.0.1:5244/p/local/Alist%20V3.md")  # noqa:E501
        self.assertEqual(object["readme"], "")
        self.assertEqual(object["header"], "")
        self.assertEqual(object["provider"], "Local")
        self.assertEqual(object["related"], None)


if __name__ == "__main__":
    unittest.main()
