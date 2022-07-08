from pathlib import Path
from textwrap import dedent

import pytest

from server import settings
from server.tools.mdformat import main


@pytest.fixture
def tmp_content_dir(tmpdir: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(
        settings, "EXTRA_CONTENT_DIRS", [*settings.EXTRA_CONTENT_DIRS, tmpdir]
    )

    return tmpdir


def test_mdformat(tmp_content_dir: Path) -> None:
    content_initial = dedent(
        """
        Before

        ```python
        lst = ["hello",
               "world",]
        ```

        <!--pytest.mark.skip-->

        ```python
        !invalid+?python
        ```

        ```js
        const isPython = false;
        ```

        After
        """
    )

    testfile = tmp_content_dir / "test.md"
    testfile.write_text(content_initial, "utf-8")

    rv = main(check=True)
    assert rv == 1
    assert testfile.read_text("utf-8") == content_initial

    rv = main()
    assert rv == 0
    assert testfile.read_text("utf-8") == dedent(
        """
        Before

        ```python
        lst = [
            "hello",
            "world",
        ]
        ```

        <!--pytest.mark.skip-->

        ```python
        !invalid+?python
        ```

        ```js
        const isPython = false;
        ```

        After
        """
    )

    rv = main(check=True)
    assert rv == 0


def test_mdformat_newlines(tmp_content_dir: Path) -> None:
    content = "Final newline will be added."
    assert not content.endswith("\n")

    testfile = tmp_content_dir / "test.md"
    testfile.write_text(content, "utf-8")

    rv = main()
    assert rv == 0
    assert testfile.read_text("utf-8").endswith("\n")


def test_mdformat_errors(tmp_content_dir: Path) -> None:
    invalid_python = dedent(
        """
    ```python
    >>> print('shell')  # Ignored
    ```

    ```python
    _ = syntax: error
    ```
    """
    )

    testfile = tmp_content_dir / "test.md"
    testfile.write_text(invalid_python, "utf-8")

    rv = main()
    assert rv == 1
    assert testfile.read_text("utf-8") == invalid_python

    rv = main(check=True)
    assert rv == 1
