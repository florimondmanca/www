import pytest

from server.web.resources import category_label, dateformat


def test_dateformat() -> None:
    assert dateformat("2020-07-23") == "Jul 23, 2020"


def test_category_label() -> None:
    assert category_label("tutorials") == "Tutorials"
    assert category_label("essays") == "Essays"
    assert category_label("retrospectives") == "Retrospectives"

    with pytest.raises(ValueError):
        category_label("doesnotexist")
