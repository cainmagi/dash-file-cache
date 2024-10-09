"""Pytest configurations
"""

import os
import logging
import multiprocess
import multiprocessing

from typing import TYPE_CHECKING

import pytest

import chromedriver_binary  # noqa: F401


def pytest_addoption(parser):
    parser.addoption(
        "--with-dash",
        action="store_true",
        help=(
            "Run the optional tests for local dash app. They require Chrome driver "
            "supports."
        ),
    )


def pytest_configure(config):
    getattr(multiprocess, "set_start_method")("spawn")
    multiprocessing.set_start_method("spawn")
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    config.addinivalue_line(
        "markers", "with_dash: run the dash test with Chrome driver."
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--with-dash"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_wdash = pytest.mark.skip(reason="need --with-dash option to run")
    for item in items:
        if "with_dash" in item.keywords:
            item.add_marker(skip_wdash)


if not TYPE_CHECKING:
    try:
        from selenium.webdriver.chrome.options import Options

        def pytest_setup_options():
            # raise TypeError(same_hook)
            # The following configuration requires the installation of chrome!
            options = Options()
            # Removes a bunch of errors on Windows, like
            # USB: usb_device_win.cc:93 Failed to read descriptors from ...
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # Do not need to configure --headless because it is included in the
            # pytest option (provided by dash_duo).
            # options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            # Configure the folder of downloaded files.
            options.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": os.path.join(
                        os.path.dirname(__file__), "temp-download"
                    )
                },
            )
            return options

    except ImportError:
        pass
