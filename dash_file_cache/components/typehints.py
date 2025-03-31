"""
Typehints
=========
@ Dash File Cache: components

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
Extra typehints used for annotating the component properties.
"""

from typing_extensions import Literal, TypedDict


__all__ = ("DownloaderURL", "DownloaderStatus")


class DownloaderURL(TypedDict):
    """The component property `Downloader(url=...)`.

    The URL used to access the data to be downloaded.

    Each time when this value is set, a download event will be triggered. After
    triggering the download event, this value will be reset by a blank string.
    """

    url: str
    """The URL used to access the data to be downloaded."""

    file_name_fallback: str
    """A maunally configured file name. If this file name is configured, it will
    be used when the file name cannot be parsed in the headers. This configuration
    is useful when the URL is from a cross-origin site."""


class DownloaderStatus(TypedDict):
    """The component property `Downloader(status=...)`.

    The status code when a downloading event is finalized.

    If multiple downloading events are triggered by the same downloader, the later
    event will overwrite the status from the former events.
    """

    type: Literal[
        "success", "error-connect", "error-config", "error-io", "error-unknown"
    ]
    """The status code of the event. If the event is successful, this value should.
    be "success" once the downloading event is finalized.
    """

    http_code: int
    """The HTTP code from the response. If the event is successful, this value should
    be in the range of 200-299.."""
