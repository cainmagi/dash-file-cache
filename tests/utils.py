# -*- coding: UTF-8 -*-
"""
Utilities
=========
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
Extra functionalities used for enhancing the tests.
"""

import os
import collections.abc
import hashlib
import contextlib
import xml.dom.minidom

from typing import Union, Optional, Any, IO

try:
    from typing import Sequence, Mapping, Callable
    from typing import Dict
except ImportError:
    from collections.abc import Sequence, Mapping, Callable
    from builtins import dict as Dict

from typing_extensions import Literal

from dash.testing.composite import DashComposite
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException


__all__ = (
    "get_file_from_test_folder",
    "get_file_from_example_folder",
    "get_svg_properties",
    "calc_hash",
    "is_eq",
    "is_eq_mapping",
    "is_eq_sequence",
    "is_mapping_with_keys",
    "attribute_value_neq",
    "wait_for_text_neq",
    "wait_for_the_attribute_value_to_equal",
    "wait_for_the_attribute_value_neq",
    "wait_for_the_attribute_value_to_be",
    "wait_for_dcc_loading",
    "wait_for",
)


def get_file_from_test_folder(file_name: str) -> str:
    """Return the path of the file in this test folder."""
    return os.path.join(os.path.dirname(__file__), file_name)


def get_file_from_example_folder(file_name: str) -> str:
    """Return the path of the file in the example folder."""
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "examples", file_name
    )


def get_svg_properties(path: str) -> Dict[str, str]:
    """Get the root properties of an SVG file.

    Arguments
    ---------
    path: `str`
        The path to the SVG file.

    Returns
    -------
    #1: `{str: str}`
        A dictionary of attribute in the root node of the SVG file.
    """
    ele = xml.dom.minidom.parse(path).getElementsByTagName("svg")
    if len(ele) < 1:
        return dict()

    return dict(
        (
            str(key),
            str(val.value) if isinstance(val, xml.dom.minidom.Attr) else str(val),
        )
        for key, val in ele[0].attributes.items()
    )


def calc_hash(
    fobj: Union[str, os.PathLike, IO[bytes]],
    salt: str = "",
    chunk_size: int = 1024 * 1024,
    method: Literal["sha256", "sha512", "sha3_256", "sha3_512", "md5"] = "sha256",
) -> str:
    """Calculate the hash code of a specific file.

    Arguments
    ---------
    fobj: `str | os.PathLike | IO[bytes]`
        A file path or a file-like object. The hash code will be calculated on the
        whole file.

    salt: `str`
        The salt used for initializing the hash.

    chunk_size: `int`
        Chunk size (B) used for calculating the hash.

    method: `"sha256" | "sha512" | "sha3_256" | "sha3_512" | "md5"`
        The method used for calculating the hash.

    Returns
    -------
    #1: `str`
        The HEX-formatted hash code calculated on `fobj`.
    """
    hashobj = hashlib.new(method)
    # Use the salt as the init value.
    if salt:
        hashobj.update(salt.encode("utf-8"))
    # Start to hash it.
    with contextlib.ExitStack() as stk:
        if isinstance(fobj, (str, os.PathLike)):
            fobj = stk.enter_context(open(fobj, "rb"))
        for byte_block in iter(lambda: fobj.read(chunk_size), b""):
            hashobj.update(byte_block)
    code = hashobj.hexdigest()
    return code


def is_eq(val: Any, ref: Any) -> bool:
    """Safely check whether `val == ref`"""
    if isinstance(ref, (str, bytes)):
        return isinstance(val, ref.__class__) and val == ref
    if isinstance(ref, collections.abc.Sequence):
        return is_eq_sequence(val, ref)
    elif isinstance(ref, collections.abc.Mapping):
        return is_eq_mapping(val, ref)
    else:
        return isinstance(val, ref.__class__) and val == ref


def is_eq_mapping(val: Any, ref: Mapping[Any, Any]) -> bool:
    """Safely check whether `val == ref`, where `ref` is a mapping."""
    if not isinstance(val, collections.abc.Mapping):
        return False
    return val == ref


def is_eq_sequence(val: Any, ref: Sequence[Any]) -> bool:
    """Safely check whether `val == ref`, where `ref` is a sequence."""
    if isinstance(val, (str, bytes)) or (not isinstance(val, collections.abc.Sequence)):
        return False
    return tuple(val) == tuple(ref)


def is_mapping_with_keys(val: Any, keys: Sequence[Any]) -> bool:
    """Check whether `val` is mapping and this mapping has keys specified by `keys`.

    If `keys` is not a sequence, will treat it as one key.
    """
    if isinstance(keys, (str, bytes)) or (
        not isinstance(keys, collections.abc.Sequence)
    ):
        keys = (keys,)
    if not isinstance(val, collections.abc.Mapping):
        return False
    return set(val.keys()) == set(keys)


class attribute_value_neq:
    """Wait-for method: attribute value does not equal to something.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(self, element: WebElement, attribute: str, value: Any) -> None:
        """Initialization.

        Arguments
        ---------
        element: `WebElement`
            The selected selenium `WebElement` where the attribtue will be listened to.

        attribtue: `str`
            The attribute name to be checked. Normally, this name should starts with
            `"data-"`.

        value: `Any`
            The value that the attribute needs to quit from. Normally, this value
            should be a string.
        """
        self.element = element
        self.attribute = attribute
        self.value = value
        self.value_type = type(value)

    def __call__(self, driver: WebDriver):
        """Wait-for method."""
        try:
            element_attribute = self.element.get_attribute(self.attribute)
            return (not isinstance(element_attribute, self.value_type)) or (
                element_attribute != self.value
            )
        except StaleElementReferenceException:
            return False


class attribute_value_to_equal:
    """Wait-for method: attribute value equals to something.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(self, element: WebElement, attribute: str, value: Any) -> None:
        """Initialization.

        Arguments
        ---------
        element: `WebElement`
            The selected selenium `WebElement` where the attribtue will be listened to.

        attribtue: `str`
            The attribute name to be checked. Normally, this name should starts with
            `"data-"`.

        value: `Any`
            The value that the attribute expects to be. Normally, this value
            should be a string.
        """
        self.element = element
        self.attribute = attribute
        self.value = value
        self.value_type = type(value)

    def __call__(self, driver: WebDriver):
        """Wait-for method."""
        try:
            element_attribute = self.element.get_attribute(self.attribute)
            return isinstance(element_attribute, self.value_type) and (
                element_attribute == self.value
            )
        except StaleElementReferenceException:
            return False


class attribute_value_to_be:
    """Wait-for method: attribute value pass the check of a function.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(
        self, element: WebElement, attribute: str, func: Callable[[Any], bool]
    ) -> None:
        """Initialization.

        Arguments
        ---------
        element: `WebElement`
            The selected selenium `WebElement` where the attribtue will be listened to.

        attribtue: `str`
            The attribute name to be checked. Normally, this name should starts with
            `"data-"`.

        func: `(Any) -> bool`
            A function accept the attribtue value as the input and return the check
            result. If this function returns `True`, it means that the check passes.
        """
        if not callable(func):
            raise TypeError('The argument "func" needs to be callable.')
        self.element = element
        self.attribute = attribute
        self.func = func

    def __call__(self, driver: WebDriver):
        """Wait-for method."""
        try:
            element_attribute = self.element.get_attribute(self.attribute)
            return self.func(element_attribute)
        except StaleElementReferenceException:
            return False


class text_to_neq:
    """Wait-for method: text value does not equal to something.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(self, element: WebElement, text: str):
        """Initialization.

        Arguments
        ---------
        element: `WebElement`
            The selected selenium `WebElement` where the attribtue will be listened to.

        text: `str`
            The value that the text needs to quit from. Normally, this value
            should be a string.
        """
        self.element = element
        self.text = text

    def __call__(self, driver):
        try:
            value = self.element.get_attribute("value")
            return str(self.element.text) != self.text or (
                value is not None and str(value) != self.text
            )
        except StaleElementReferenceException:
            return False


class wait_func:
    """Wait-for method: text value does not equal to something.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(self, func: Callable[[], bool]):
        """Initialization.

        Arguments
        ---------
        func: `() -> bool`
            The function to be waited. If `func()` returns `True`, the waiting will be
            finished.
        """
        self.func = func

    def __call__(self, driver):
        try:
            return self.func()
        except StaleElementReferenceException:
            return False


def wait_for_text_neq(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    text: str = "",
    timeout: Optional[int] = None,
) -> None:
    """Explicit wait until the element's text does not equal the `text`.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    text: `str`
        The value that the text needs to quit from. Normally, this value should
        be a string.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    dash_duo._wait_for(
        text_to_neq(dash_duo.find_element(selector, by), text),
        timeout=timeout,
        msg=(
            "timeout {0}s => waiting for the element {1} until the text equals to "
            "{2}.".format(timeout or dash_duo._wait_timeout, selector, text)
        ),
    )


def wait_for_the_attribute_value_neq(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    attribute: str = "data-any",
    value: Any = "",
    timeout: Optional[int] = None,
) -> None:
    """Select an element, and wait until its attribute does not equal to the specific
    value.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    attribtue: `str`
        The attribute name to be checked. Normally, this name should starts with
        `"data-"`.

    value: `Any`
        The value that the attribute needs to quit from. Normally, this value should
        be a string.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    dash_duo._wait_for(
        attribute_value_neq(dash_duo.find_element(selector, by), attribute, value),
        timeout=timeout,
        msg=(
            "timeout {0}s => waiting for the element {1} until the attribute {2} is "
            "not {3}.".format(
                timeout or dash_duo._wait_timeout, selector, attribute, value
            )
        ),
    )


def wait_for_the_attribute_value_to_equal(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    attribute: str = "data-any",
    value: Any = "",
    timeout: Optional[int] = None,
) -> None:
    """Select an element, and wait until its attribute equals to the specific value.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    attribtue: `str`
        The attribute name to be checked. Normally, this name should starts with
        `"data-"`.

    value: `Any`
        The value that the attribute expects to be. Normally, this value should be a
        string.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    dash_duo._wait_for(
        attribute_value_to_equal(dash_duo.find_element(selector, by), attribute, value),
        timeout=timeout,
        msg=(
            "timeout {0}s => waiting for the element {1} until the attribute {2} is "
            "not {3}.".format(
                timeout or dash_duo._wait_timeout, selector, attribute, value
            )
        ),
    )


def wait_for_the_attribute_value_to_be(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    attribute: str = "data-any",
    func: Optional[Callable[[Any], bool]] = None,
    timeout: Optional[int] = None,
) -> None:
    """Select an element, and wait until its attribute equals to the specific value.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    attribtue: `str`
        The attribute name to be checked. Normally, this name should starts with
        `"data-"`.

    func: `((Any) -> bool) | None`
        The validator function. The input value is the attribute value. If this
        function returns `True`, the check will pass.

        If this function is not specified, will not wait for anything and return
        immediately.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    if func is None:
        return
    dash_duo._wait_for(
        attribute_value_to_be(dash_duo.find_element(selector, by), attribute, func),
        timeout=timeout,
        msg=(
            "timeout {0}s => waiting for the element {1} until the attribute {2} passes"
            "the test function {3}.".format(
                timeout or dash_duo._wait_timeout, selector, attribute, str(func)
            )
        ),
    )


def wait_for_dcc_loading(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    timeout: Optional[int] = None,
) -> None:
    """Select an element, and wait until it quits from the is-loading state.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    dash_duo._wait_for(
        attribute_value_neq(
            dash_duo.find_element(selector, by), "data-dash-is-loading", "true"
        ),
        timeout=None,
        msg=(
            "timeout {0}s => waiting for the element {1} to be loaded.".format(
                timeout or dash_duo._wait_timeout, selector
            )
        ),
    )


def wait_for(
    dash_duo: DashComposite,
    func: Optional[Callable[[], bool]] = None,
    timeout: Optional[int] = None,
) -> None:
    """The general `wait_for` method for `dash_duo`.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    func: `(() -> bool) | None`
        The validator function. The input value is the attribute value. If this
        function returns `True`, the check will pass.

        If this function is not specified, will not wait for anything and return
        immediately.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    if func is None:
        return
    dash_duo._wait_for(
        wait_func(func),
        timeout=timeout,
        msg=(
            "timeout {0}s => waiting for the function {1}.".format(
                timeout or dash_duo._wait_timeout, str(func)
            )
        ),
    )
