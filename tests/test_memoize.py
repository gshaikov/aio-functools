import pytest
import asyncio
from contextlib import contextmanager
from unittest.mock import Mock
from aiofunctools.memoize import memoize


this_line_was_executed = Mock()


@contextmanager
def checkpoint(mockpoint):
    yield mockpoint
    mockpoint.reset_mock()


@memoize
async def example_coro(*args):
    this_line_was_executed()
    await asyncio.sleep(1)
    return args


@pytest.mark.asyncio
async def test_memoize():
    with checkpoint(this_line_was_executed) as point:
        result = await example_coro(1, 2, 3)
        assert result == (1, 2, 3)
        point.assert_called_once()

    with checkpoint(this_line_was_executed) as point:
        result = await example_coro(1, 2, 3)
        assert result == (1, 2, 3)
        point.assert_not_called()

    with checkpoint(this_line_was_executed) as point:
        result = await example_coro(1, 2, 3, 4)
        assert result == (1, 2, 3, 4)
        point.assert_called_once()


@pytest.mark.asyncio
async def test_memoize_race_condition():
    with checkpoint(this_line_was_executed) as point:
        coro1 = example_coro(1)
        coro2 = example_coro(1)
        result = await asyncio.gather(coro1, coro2)
        assert result == [(1,), (1,)]
        point.assert_called_once()
