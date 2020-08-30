from server.resources import dateformat


def test_dateformat() -> None:
    assert dateformat("2020-07-23") == "Jul 23, 2020"
