from server.di import resolve
from server.web.templating import Templates


def test_dateformat() -> None:
    templates = resolve(Templates)

    template = templates.from_string("{{ value | dateformat }}")
    assert template.render(value="2020-07-23") == "Jul 23, 2020"
