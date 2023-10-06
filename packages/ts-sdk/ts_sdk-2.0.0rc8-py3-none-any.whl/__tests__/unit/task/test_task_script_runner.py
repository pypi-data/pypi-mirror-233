import os
from io import StringIO

import pytest

from __tests__.unit.util import __before
from ts_sdk.task.__task_script_runner import (
    construct_shadow_print,
    should_override_builtin_print,
)
from ts_sdk.task.__util_adapters.communication_format import (
    COMMUNICATION_FORMAT_ENV_KEY,
    CommunicationFormat,
)


def __set_communication_format(communication_format):
    def applicator():
        os.environ.update(
            {
                COMMUNICATION_FORMAT_ENV_KEY: communication_format.value,
            }
        )

    return applicator


v0 = __before(__set_communication_format(CommunicationFormat.V0))
v1 = __before(__set_communication_format(CommunicationFormat.V1))
v2 = __before(__set_communication_format(CommunicationFormat.V2))
vZ = __before(__set_communication_format(CommunicationFormat.VZ))


class LogMock:
    def __init__(self):
        self.lines = []

    def log(self, *args, **kwargs):
        self.lines.append({"args": args, "kwargs": kwargs})

    def flush(self):
        lines = self.lines
        self.lines = []
        return lines


def test_shadow_print_goes_to_print_if_file_is_provided():
    fake_file = StringIO()
    fake_logger = LogMock()
    assert fake_file.getvalue() == ""
    assert fake_logger.flush() == []
    shadow_print = construct_shadow_print(fake_logger)
    shadow_print("foo", "bar", sep="//", end="!", file=fake_file, flush=True)
    assert fake_file.getvalue() == "foo//bar!"
    assert fake_logger.flush() == []


def test_shadow_print_goes_to_logger():
    fake_logger = LogMock()
    assert fake_logger.flush() == []
    shadow_print = construct_shadow_print(fake_logger)
    shadow_print("foo", "bar", sep="//", end="!", flush=True)
    assert fake_logger.flush() == [{"args": ("foo", "bar"), "kwargs": {"sep": "//"}}]


@v0
def test_should_override_builtin_print_v0():
    assert should_override_builtin_print() is True


@v1
def test_should_override_builtin_print_v1():
    assert should_override_builtin_print() is True


@v2
def test_should_override_builtin_print_v2():
    assert should_override_builtin_print() is False


@vZ
def test_should_override_builtin_print_unrecognized():
    with pytest.raises(NotImplementedError):
        should_override_builtin_print()
