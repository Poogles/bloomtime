import time
import logging

import pytest

import bloomtime.bloomtime as bloomtime


@pytest.fixture
def bloomtime_fixture():
    return bloomtime.BloomTime(1000, 0.001)


def test_set(bloomtime_fixture, caplog):
    caplog.set_level(logging.DEBUG)

    bloomtime_fixture.set('foo')
    # We know 9 hashes should be set.
    total = 0
    for i in bloomtime_fixture._container:
        if i > 0:
            total += 1
    assert total == 9


def test_ttl_set(bloomtime_fixture, mocker, caplog):
    caplog.set_level(logging.DEBUG)

    TTL = 400
    bloomtime_fixture.set('foo', ttl=TTL)
    assert bloomtime_fixture.get('foo') is True

    mock_time = mocker.patch.object(bloomtime, 'time')
    # Return a time that's in the future past the end of the TTL
    EXPIRED_TIME = time.time() + TTL + 1
    mock_time.time.return_value = EXPIRED_TIME

    # TTL has now expired, check it's False.
    assert bloomtime_fixture.get('foo') is False


def test_common_result(bloomtime_fixture, mocker, caplog):
    caplog.set_level(logging.DEBUG)
    # Set foo to be in the filter.
    bloomtime_fixture.set('foo', ttl=400)
    # simulate a couple of hash collisions by altering some buckets.
    # because we're using the builtin hash we need to do this in this process
    # rather than just hard coding some values.
    collisions = 0
    for pos, i in enumerate(bloomtime_fixture._container):
        if i > 0:
            bloomtime_fixture._container[pos] = 987
            collisions += 1
        # We only want a couple of collisions.
        if collisions == 2:
            break

    assert bloomtime_fixture.get('foo') is True


def test_contains_methods(bloomtime_fixture):
    # This would raise a syntax error without __contains__.
    bloomtime_fixture.set('foo')
    assert "foo" in bloomtime_fixture


def test_benchmark_set(bloomtime_fixture, benchmark):
    benchmark(bloomtime_fixture.set, 'foo')


def test_benchmark_get(bloomtime_fixture, benchmark):
    bloomtime_fixture.set('foo')
    benchmark(bloomtime_fixture.get, 'foo')
