from starlette.testclient import TestClient


def test_redirect_dot_com(client: TestClient) -> None:
    url = "http://blog.florimondmanca.com/page"
    r = client.get(url, allow_redirects=False)
    assert r.status_code == 301
    assert r.headers["Location"] == "http://blog.florimond.dev/page"


def test_redirect_dot_dev(client: TestClient) -> None:
    url = "http://blog.florimond.dev/page"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["Location"] == "http://florimond.dev/blog/page"


def test_redirect_dot_dev_root(client: TestClient) -> None:
    url = "http://blog.florimond.dev"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["Location"] == "http://florimond.dev/blog/"


def test_redirect_article(client: TestClient) -> None:
    url = "http://florimond.dev/blog/let-the-journey-begin"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 301
    assert (
        resp.headers["Location"]
        == "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin"
    )
