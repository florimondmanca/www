import pytest

from server.di import resolve
from server.web.templating import Templates


def test_dateformat() -> None:
    templates = resolve(Templates)

    template = templates.from_string("{{ value | dateformat }}")
    assert template.render(value="2020-07-23") == "Jul 23, 2020"


def test_category_label() -> None:
    templates = resolve(Templates)

    template = templates.from_string("{{ value | category_label }}")
    assert template.render(value="tutorials") == "Tutorials"
    assert template.render(value="essays") == "Essays"
    assert template.render(value="retrospectives") == "Retrospectives"

    with pytest.raises(ValueError):
        template.render(value="doesnotexist")
