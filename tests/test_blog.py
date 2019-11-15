from starlette.testclient import TestClient


def test_root(client: TestClient) -> None:
    url = "http://florimond.dev/blog/"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


def test_article(client: TestClient) -> None:
    urls = [
        "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin",
        "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/",
        "http://florimond.dev/blog/articles/2018/07/let-the-journey-begin/index.html",
    ]
    responses = [client.get(url, allow_redirects=False) for url in urls]
    for resp in responses:
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
    unique_contents = {resp.text for resp in responses}
    assert len(unique_contents) == 1


def test_tag(client: TestClient) -> None:
    url = "http://florimond.dev/blog/tag/python"
    resp = client.get(url, allow_redirects=False)
    assert resp.status_code == 200, resp.url
    assert "text/html" in resp.headers["content-type"]


def test_not_found(client: TestClient) -> None:
    url = "http://florimond.dev/blog/foo"
    resp = client.get(url)
    assert resp.status_code == 404
    assert "text/html" in resp.headers["content-type"]
