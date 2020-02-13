import pytest


def test_get_quotes(api):
    code, quotes = api.get_quotes()
    assert code == 200
    assert type(quotes) == dict


def test_filtered_quotes(api):
    code, quotes = api.get_filtered_quotes('power')
    assert code == 200
    assert type(quotes) == dict
