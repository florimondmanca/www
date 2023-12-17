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


class RelParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rels: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attr = dict(attrs)

        if "rel" in attr:
            self.rels.append((tag, attr["rel"], attr["href"]))


def find_webmention_url(html: str) -> str | None:
    parser = RelParser()
    parser.feed(html)

    for tag, rel, href in parser.rels:
        if tag == "link" and rel == "webmention":
            return href

    return None


def find_rel_me_links(html: str) -> list[str]:
    parser = RelParser()
    parser.feed(html)

    return [href for tag, rel, href in parser.rels if tag == "a" and rel == "me"]


class HCardParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hcard: dict = {}
        self._in_hcard = False
        self._field = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attr = dict(attrs)

        classattr = attr.get("class", "")

        if "h-card" in classattr:
            self._in_hcard = True

        if self._in_hcard:
            if tag == "img" and "u-photo" in classattr:
                self.hcard["u-photo"] = attr["src"]

            if tag == "a" and "u-uid" in classattr:
                self.hcard["u-uid"] = attr["href"]

            if tag == "a" and "u-url" in classattr:
                self.hcard["u-url"] = attr["href"]

            if "p-note" in classattr:
                self._field = "p-note"

    def handle_data(self, data: str) -> None:
        if self._field:
            self.hcard[self._field] = data

    def handle_endtag(self, _: str) -> None:
        if self._field:
            self._field = ""


def parse_hcard(html: str) -> dict:
    parser = HCardParser()
    parser.feed(html)
    return parser.hcard


class HEntryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hentry: dict = {}
        self._in_hentry = False
        self._field = ""

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attr = dict(attrs)

        classattr = attr.get("class", "")

        if tag == "article" and "h-entry" in classattr:
            self._in_hentry = True

        if self._in_hentry:
            if tag == "h1" and "p-name" in classattr:
                assert not self._field
                self._field = "p-name"

            if "p-summary" in classattr:
                assert not self._field
                self._field = "p-summary"

            if tag == "a" and "p-author" in classattr:
                self.hentry["p-author"] = attr["href"]

            if tag == "a" and "h-card" in classattr:
                self.hentry["h-card"] = attr["href"]

            if tag == "a" and "u-url" in classattr:
                self.hentry["u-url"] = attr["href"]

            if tag == "a" and "p-category" in classattr:
                self.hentry.setdefault("p-category", []).append(attr["href"])

            if tag == "time" and "dt-published" in classattr:
                self.hentry["dt-published"] = attr["datetime"]

            if "e-content" in classattr:
                assert not self._field
                self._field = "e-content"

    def handle_data(self, data: str) -> None:
        if self._field:
            self.hentry[self._field] = data

    def handle_endtag(self, _: str) -> None:
        if self._field:
            self._field = ""


def parse_hentry(html: str) -> dict:
    parser = HEntryParser()
    parser.feed(html)
    return parser.hentry
