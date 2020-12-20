from server.tools.imgoptimize import main


def test_imgoptimize() -> None:
    assert main(check=True) == 0
