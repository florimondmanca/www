from html.parser import HTMLParser
from xml.dom import minidom


def load_xml_from_string(content: str) -> minidom.Document:
    return minidom.parseString(content)


class HeadMetaHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_head = False
        self.meta: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "head":
            self.in_head = True
        elif self.in_head and tag == "meta":
            self.meta.append({key: value for key, value in attrs if value})

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self.in_head = False


def find_meta_tags(html: str) -> list:
    parser = HeadMetaHTMLParser()
    parser.feed(html)
    return parser.meta


class StartTagParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.start_tag: tuple[str, dict] | None = None

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if self.start_tag is None:
            self.start_tag = (tag, dict(attrs))


def get_start_tag(html: str) -> tuple[str, dict]:
    parser = StartTagParser()
    parser.feed(html)
    assert parser.start_tag is not None
    return parser.start_tag
