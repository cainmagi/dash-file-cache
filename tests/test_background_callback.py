# -*- coding: UTF-8 -*-
"""
Test the background callback demo
=================================
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
The tests for the `background_callback.py` demo. These tests will run a browser
enmulator powered by `selenium` and `dash.testing`. The basic functionalities of the
demo will be checked one by one.
"""

import logging
import importlib.util
import multiprocess

try:
    from typing import Generator
except ImportError:
    from collections.abc import Generator

import pytest

import dash
from dash.testing.composite import DashComposite
from selenium.webdriver.remote.webelement import WebElement

from .utils import (
    get_file_from_example_folder,
    get_svg_properties,
    wait_for_the_attribute_value_to_be,
)


__all__ = ("TestBackgroundCallback",)


@pytest.mark.with_dash
class TestBackgroundCallback:
    """Test the rendering and the usage of the single-process cache in a Dash app."""

    @pytest.fixture(scope="class")
    def dash_app(self) -> Generator[dash.Dash, None, None]:
        log = logging.getLogger("dash_file_cache.test")
        log.info("Initialize the Dash app.")
        _module = importlib.import_module("examples.background_callback")
        wrapped_app = _module.wrapped_app
        proc_manager = getattr(
            multiprocess.context._default_context.get_context("spawn"), "Manager"
        )()
        wrapped_app.load(proc_manager.Queue(1))
        app = wrapped_app.app

        yield app
        log.info("Remove the Dash app.")
        del app
        del wrapped_app
        del _module

    def test_background_callback(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the functionalities of caching the data shared by multiple processes.

        This test will click several buttons triggering the callbacks.
        """
        log = logging.getLogger("dash_file_cache.test")

        # Start a dash app contained as the variable `app`
        dash_duo.start_server(dash_app)

        for btn_id, cache_type in (
            ("#btn-strio", "StringIO"),
            ("#btn-bytesio", "BytesIO"),
            ("#btn-path", "str"),
        ):
            btn: WebElement = dash_duo.find_element(btn_id)

            btn.click()
            dash_duo.wait_for_text_to_equal("#type", cache_type)
            log.info("Get the cache type: {0}".format(cache_type))

            ele_addr: WebElement = dash_duo.find_element("#addr")
            text_addr = ele_addr.text
            log.info("Get the cached file addr: {0}".format(text_addr))
            assert isinstance(text_addr, str) and text_addr.startswith("/cached-data")

            wait_for_the_attribute_value_to_be(
                dash_duo,
                selector="#cache",
                attribute="src",
                func=lambda src: isinstance(src, str) and src.endswith(text_addr),
            )
            ele_img: WebElement = dash_duo.find_element("#cache")
            img_width = int(ele_img.get_attribute("width"))
            img_height = int(ele_img.get_attribute("height"))
            svg_props = get_svg_properties(
                get_file_from_example_folder("test_image.svg")
            )
            log.info(
                "Get image size: width={0}, height={1}".format(img_width, img_height)
            )
            if "width" in svg_props:
                assert str(img_width) == svg_props["width"]
            else:
                assert img_width > 32
            if "height" in svg_props:
                assert str(img_height) == svg_props["height"]
            else:
                assert img_height > 32
