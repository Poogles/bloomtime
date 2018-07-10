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
    # We know the hashes for foo on a 1000 item container
    assert bloomtime_fixture._container[885] > 1
    assert bloomtime_fixture._container[266] > 1
    assert bloomtime_fixture._container[647] > 1
    assert bloomtime_fixture._container[28] > 1
    assert bloomtime_fixture._container[409] > 1
    assert bloomtime_fixture._container[790] > 1
    assert bloomtime_fixture._container[171] > 1
    assert bloomtime_fixture._container[552] > 1
    assert bloomtime_fixture._container[837] > 1


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


def test_contains_methods(bloomtime_fixture):
    # This would raise a syntax error without __contains__.
    bloomtime_fixture.set('foo')
    assert "foo" in bloomtime_fixture


def test_benchmark_set(bloomtime_fixture, benchmark):
    benchmark(bloomtime_fixture.set, 'foo')


def test_benchmark_get(bloomtime_fixture, benchmark):
    bloomtime_fixture.set('foo')
    benchmark(bloomtime_fixture.get, 'foo')
