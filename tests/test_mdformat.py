from pathlib import Path
from textwrap import dedent

from server.tools.mdformat import main


def test_mdformat(tmpdir: Path) -> None:
    content_initial = dedent(
        """
        Before

        ```python
        lst = ["hello",
               "world",]
        ```

        After
        """
    )

    testfile = tmpdir / "test.md"
    testfile.write_text(content_initial, "utf-8")

    rv = main([testfile], check=True)
    assert rv == 1
    assert testfile.read_text("utf-8") == content_initial

    rv = main([testfile], check=False)
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

        After
        """
    )

    rv = main([testfile], check=True)
    assert rv == 0


def test_mdformat_empty(tmpdir: Path) -> None:
    no_python = dedent(
        """
        No Python code blocks here.

        ```javascript
        console.log('hello, world!!');
        ```
    """
    )

    testfile = tmpdir / "test.md"
    testfile.write_text(no_python, "utf-8")

    rv = main([testfile], check=False)
    assert rv == 0
    assert testfile.read_text("utf-8") == no_python

    rv = main([testfile], check=True)
    assert rv == 0


def test_mdformat_errors(tmpdir: Path) -> None:
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

    testfile = tmpdir / "test.md"
    testfile.write_text(invalid_python, "utf-8")

    rv = main([testfile], check=False)
    assert rv == 1
    assert testfile.read_text("utf-8") == invalid_python

    rv = main([testfile], check=True)
    assert rv == 1
