from starlette.testclient import TestClient


def test_redirect_root(client: TestClient) -> None:
    url = "http://blog.florimond.dev/"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["Location"] == "http://florimond.dev/blog/"


def test_redirect_root_no_slash(client: TestClient) -> None:
    url = "http://blog.florimond.dev"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["Location"] == "http://florimond.dev/blog/"


def test_redirect_article(client: TestClient) -> None:
    url = "http://blog.florimond.dev/let-the-journey-begin"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 301
    assert (
        resp.headers["Location"]
        == "http://florimond.dev/blog/articles/let-the-journey-begin"
    )
