from xml.dom import minidom


def load_xml_from_string(content: str) -> None:
    minidom.parseString(content)
