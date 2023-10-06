import os
from unittest.mock import patch

import pytest

from __tests__.unit.util import __before
from ts_sdk.task.__util_adapters.communication_format import (
    COMMUNICATION_FORMAT_ENV_KEY,
    CommunicationFormat,
)
from ts_sdk.task import __util_ts_api as api


def __prepare_v0_test():
    os.unsetenv("KERNEL_ENDPOINT")
    os.environ.update(
        {
            COMMUNICATION_FORMAT_ENV_KEY: CommunicationFormat.V0.value,
        }
    )


def __prepare_v1_test():
    os.environ.update(
        {
            COMMUNICATION_FORMAT_ENV_KEY: CommunicationFormat.V1.value,
            "KERNEL_ENDPOINT": "https://localhost:1234",
        }
    )


v0 = __before(__prepare_v0_test)
v1 = __before(__prepare_v1_test)


@v0
def test_get_ts_api_in_communication_format_no_kernel():
    with pytest.raises(NotImplementedError):
        api.get_api_url()


@v1
def test_get_ts_api_in_communication_format_with_a_path():
    url = api.get_api_url("/v1/command")
    assert url == "https://localhost:1234/api/v1/command"


@v1
def test_get_ts_api_in_communication_format_with_a_path_no_leading_slash():
    url = api.get_api_url("v1/command")
    assert url == "https://localhost:1234/api/v1/command"


@v1
def test_get_ts_api_in_communication_format_with_a_bad_path():
    with pytest.raises(ValueError):
        api.get_api_url(10)


@v0
def test_get_v0_fails():
    with pytest.raises(NotImplementedError):
        api.get("")


@v1
@patch("requests.get")
def test_get_v1_passes_arguments(get_mock):
    api.get("/foo", {"foo": "bar"}, allow_redirects=True)
    args, kwargs = get_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {
        "allow_redirects": True,
        "params": {"foo": "bar"},
        "verify": False,
    }


@v1
@patch("requests.get")
def test_get_v1_override_verify(get_mock):
    api.get("/foo", {"foo": "bar"}, verify=True)
    args, kwargs = get_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"params": {"foo": "bar"}, "verify": True}


@v0
def test_delete_v0_fails():
    with pytest.raises(NotImplementedError):
        api.delete("")


@v1
@patch("requests.delete")
def test_delete_v1_passes_arguments(delete_mock):
    api.delete("/foo", allow_redirects=True)
    args, kwargs = delete_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"allow_redirects": True, "verify": False}


@v1
@patch("requests.delete")
def test_delete_v1_override_verify(delete_mock):
    api.delete("/foo", verify=True)
    args, kwargs = delete_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"verify": True}


@v0
def test_patch_v0_fails():
    with pytest.raises(NotImplementedError):
        api.patch("")


@v1
@patch("requests.patch")
def test_patch_v1_passes_arguments(patch_mock):
    api.patch("/foo", {"foo": "bar"}, allow_redirects=True)
    args, kwargs = patch_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"allow_redirects": True, "data": {"foo": "bar"}, "verify": False}


@v1
@patch("requests.patch")
def test_patch_v1_override_verify(patch_mock):
    api.patch("/foo", {"foo": "bar"}, verify=True)
    args, kwargs = patch_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"data": {"foo": "bar"}, "verify": True}


@v0
def test_post_v0_fails():
    with pytest.raises(NotImplementedError):
        api.post("")


@v1
@patch("requests.post")
def test_post_v1_passes_arguments(post_mock):
    api.post("/foo", {"foo": "bar"}, {"bar": "foo"}, allow_redirects=True)
    args, kwargs = post_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {
        "allow_redirects": True,
        "data": {"foo": "bar"},
        "json": {"bar": "foo"},
        "verify": False,
    }


@v1
@patch("requests.post")
def test_post_v1_override_verify(post_mock):
    api.post("/foo", {"foo": "bar"}, {"bar": "foo"}, verify=True)
    args, kwargs = post_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"data": {"foo": "bar"}, "json": {"bar": "foo"}, "verify": True}


@v0
def test_put_v0_fails():
    with pytest.raises(NotImplementedError):
        api.put("")


@v1
@patch("requests.put")
def test_put_v1_passes_arguments(put_mock):
    api.put("/foo", {"foo": "bar"}, allow_redirects=True)
    args, kwargs = put_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"allow_redirects": True, "data": {"foo": "bar"}, "verify": False}


@v1
@patch("requests.put")
def test_put_v1_override_verify(put_mock):
    api.put("/foo", {"foo": "bar"}, verify=True)
    args, kwargs = put_mock.call_args
    assert args[0] == "https://localhost:1234/api/foo"
    assert kwargs == {"data": {"foo": "bar"}, "verify": True}
