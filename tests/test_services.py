# -*- coding: UTF-8 -*-
"""
Test services
=============
@ Dash File Cache - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
Test for services without launching the dash emulator. These tests will only focus
on the functionalities of the services.
"""

import os
import io
import collections.abc
import logging
import importlib.util

try:
    from typing import Generator
except ImportError:
    from collections.abc import Generator

import pytest

import flask
import flask.testing
from flask import url_for

from .utils import calc_hash


__all__ = ("TestServices",)


class TestServices:
    """Test the functionalities of the flask services."""

    @pytest.fixture(scope="class")
    def app(self) -> Generator[flask.Flask, None, None]:
        log = logging.getLogger("dash_file_cache.test")
        log.info("Initialize the Flask app.")
        _module = importlib.import_module("examples.flask_services")
        app = _module.app
        yield app
        log.info("Remove the Flask app.")
        del app
        del _module

    def test_service_metadata(self, client: flask.testing.FlaskClient) -> None:
        """Test the services of getting metadata."""
        log = logging.getLogger("dash_file_cache.test")

        # Get the list of available files.
        resp = client.get(url_for("index"))
        assert resp.status_code < 400
        assert resp.is_json
        file_list = resp.json
        assert isinstance(file_list, collections.abc.Mapping) and "files" in file_list
        assert len(file_list["files"]) > 1
        log.info("The list of files: {0}".format(file_list["files"]))

        # Get the first two files.
        for idx in (0, 1):
            resp = client.get(
                url_for("file"), query_string={"name": file_list["files"][idx]}
            )
            assert resp.status_code < 400
            assert resp.is_json
            info = resp.json
            assert isinstance(info, collections.abc.Mapping) and str(
                info.get("mime_type", "")
            ).startswith("image/svg")
            log.info("Information of the file: {0}".format(info))

    def test_service_get_file(self, client: flask.testing.FlaskClient) -> None:
        """Test the services of getting a file."""
        log = logging.getLogger("dash_file_cache.test")

        # Get the list of available files.
        resp = client.get(url_for("index"))
        assert resp.status_code < 400
        assert resp.is_json
        file_list = resp.json
        assert isinstance(file_list, collections.abc.Mapping) and "files" in file_list
        assert len(file_list["files"]) > 1

        # Get the file info.
        file_info = list()
        for idx in (0, 1):
            _file_name = file_list["files"][idx]
            resp = client.get(
                url_for("file"), query_string={"name": file_list["files"][idx]}
            )
            assert resp.status_code < 400
            assert resp.is_json and resp.json is not None
            _data = dict(resp.json)
            _data["name"] = _file_name
            file_info.append(_data)

        # Get the first file.
        resp = client.post(url_for("file"), query_string={"name": file_info[0]["name"]})
        assert resp.status_code < 400
        assert resp.is_json and resp.json is not None
        _addr = resp.json["addr"]
        log.info("Get the file address: {0}".format(_addr))

        resp = client.get(_addr)
        assert resp.status_code < 400
        assert resp.is_streamed
        hash_resp = calc_hash(io.BytesIO(resp.data))
        assert hash_resp == calc_hash(file_info[0]["path"])
        log.info("Fetched file is verified: {0}".format(hash_resp))

        # The same address should not be used for another time.
        resp = client.get(_addr)
        assert resp.status_code == 404
        assert resp.is_json and resp.json is not None
        log.info("Expect the error: {0}".format(resp.json["error"]))

        # Try to deliberately exceed the cache size.
        resp = client.post(url_for("file"), query_string={"name": file_info[0]["name"]})
        assert resp.status_code < 400
        assert resp.is_json and resp.json is not None
        _addr1 = resp.json["addr"]

        resp = client.post(url_for("file"), query_string={"name": file_info[1]["name"]})
        assert resp.status_code < 400
        assert resp.is_json and resp.json is not None
        _addr2 = resp.json["addr"]

        resp = client.get(_addr1)
        assert resp.status_code == 404
        assert resp.is_json and resp.json is not None
        log.info("Expect the error: {0}".format(resp.json["error"]))

        resp = client.get(_addr2)
        assert resp.status_code < 400
        assert resp.is_streamed
        hash_resp = calc_hash(io.BytesIO(resp.data))
        assert hash_resp == calc_hash(file_info[1]["path"])
        log.info("Fetched file is verified: {0}".format(hash_resp))

    def test_service_download_file(self, client: flask.testing.FlaskClient) -> None:
        """Test the services of getting a file."""
        log = logging.getLogger("dash_file_cache.test")

        # Get the list of available files.
        resp = client.get(url_for("index"))
        assert resp.status_code < 400
        assert resp.is_json
        file_list = resp.json
        assert isinstance(file_list, collections.abc.Mapping) and "files" in file_list
        assert len(file_list["files"]) > 1

        # Get the file info.
        file_info = list()
        for idx in (0, 1):
            _file_name = file_list["files"][idx]
            resp = client.get(
                url_for("file"), query_string={"name": file_list["files"][idx]}
            )
            assert resp.status_code < 400
            assert resp.is_json and resp.json is not None
            _data = dict(resp.json)
            _data["name"] = _file_name
            file_info.append(_data)

        # Download the first image.
        resp = client.post(
            url_for("file"),
            query_string={"name": file_info[0]["name"], "download": True},
        )
        assert resp.status_code < 400
        assert resp.is_json and resp.json is not None
        _addr = resp.json["addr"]
        log.info("Get the file address: {0}".format(_addr))

        resp = client.get(_addr)
        assert resp.status_code < 400
        assert resp.is_streamed
        assert resp.content_type == "application/octet-stream"
        content_disposition = resp.headers.get("content-disposition")
        assert content_disposition is not None
        file_name = content_disposition[(content_disposition.find("filename=") + 9) :]
        assert file_name == os.path.split(file_info[0]["path"])[-1]
        hash_resp = calc_hash(io.BytesIO(resp.data))
        assert hash_resp == calc_hash(file_info[0]["path"])
        log.info("Downloaded file is verified: {0}".format(hash_resp))
