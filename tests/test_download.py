# -*- coding: UTF-8 -*-
"""
Test downloading the cached file
================================
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
The tests for the `download_file.py` demo. These tests will run a browser emulator
powered by `selenium` and `dash.testing`. The basic functionalities of the demo
will be checked one by one.
"""

import os
import logging
import importlib.util

try:
    from typing import Generator
except ImportError:
    from collections.abc import Generator

import pytest

import dash
from dash.testing.composite import DashComposite
from selenium.webdriver.remote.webelement import WebElement

from .utils import wait_for, calc_hash, get_file_from_example_folder


__all__ = ("TestTempFileCache",)


@pytest.mark.with_dash
class TestTempFileCache:
    """Test the rendering and the usage of the temporary file cache in a Dash app."""

    @pytest.fixture(scope="class")
    def dash_app(self) -> Generator[dash.Dash, None, None]:
        log = logging.getLogger("dash_file_cache.test")
        log.info("Initialize the Dash app.")
        _module = importlib.import_module("examples.download_file")
        wrapped_app = _module.wrapped_app
        wrapped_app.load()
        app = wrapped_app.app
        yield app
        log.info("Remove the Dash app.")
        del app
        del wrapped_app
        del _module

    def test_download_file(self, dash_duo: DashComposite, dash_app: dash.Dash) -> None:
        """Test the functionalities of downloading a cached file.

        This test will click several buttons triggering the callbacks.
        """
        log = logging.getLogger("dash_file_cache.test")

        # Start a dash app contained as the variable `app`
        dash_duo.start_server(dash_app)

        btn: WebElement = dash_duo.find_element("#btn")

        btn.click()
        dash_duo.wait_for_text_to_equal("#type", "str")
        log.info("Cached file is ready.")

        ele_addr: WebElement = dash_duo.find_element("#addr")
        text_addr = ele_addr.text
        log.info("Get the cached file addr: {0}".format(text_addr))
        assert isinstance(text_addr, str) and text_addr.startswith("/cached-data")

        hash_src = calc_hash(get_file_from_example_folder("test_image.svg"))
        dl_file_path = os.path.join(dash_duo.download_path, "test_image.svg")
        wait_for(dash_duo, (lambda: os.path.isfile(dl_file_path)))
        assert hash_src == calc_hash(dl_file_path)
        log.info("Downloaded file is verified: {0}".format(hash_src))
