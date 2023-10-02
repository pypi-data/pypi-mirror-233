"""Tests for `pyauxlib.utils.timer`."""
import logging
import time

from pyauxlib.utils.timer import Timer


def test_timer() -> None:
    """Test the manual usage of the Timer."""
    # Test initialization
    logger = logging.getLogger(__name__)
    timer = Timer(logger=logger)
    assert timer.filename is None
    assert timer.time_func == time.time
    assert isinstance(timer.logger, logging.Logger)
    assert timer.where_output is not None
    assert timer.running is False

    # Test start and stop
    timer.start()
    assert timer.running is True
    assert hasattr(timer, "start_time")  # type: ignore[unreachable]
    time.sleep(1)  # wait for 1 second to ensure the elapsed time is non-zero
    elapsed_time = timer.stop()
    assert timer.running is False
    assert hasattr(timer, "stop_time")
    assert elapsed_time > 0

    # Test reset
    timer.reset()
    assert not hasattr(timer, "start_time")
    assert not hasattr(timer, "stop_time")


def test_timer_context_manager() -> None:
    """Test the context manager usage."""
    with Timer() as t:
        time.sleep(1)  # wait for 1 second to ensure the elapsed time is non-zero
        t.add_timestamp("#1")
    assert hasattr(t, "stop_time")


def test_timer_decorator() -> None:
    """Test the decorator usage."""
    # Decorator usage
    timer = Timer()

    @timer
    def some_function() -> None:
        time.sleep(1)  # wait for 1 second to ensure the elapsed time is non-zero

    some_function()
    assert hasattr(timer, "stop_time")
