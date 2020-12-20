from server.tools.imgsize import main


def test_imgsize() -> None:
    assert main() == 0
