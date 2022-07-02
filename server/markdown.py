from xml.etree import ElementTree as etree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ImageFigcaptions(Extension):
    """
    A Python-Markdown extension that renders the caption provided to images.

    Example
    -------

    Input:
        ![Some caption](path/to/image.png))

    Output:
        <div class="p-markdown-image">
            <img src="/path/to/mage.png" alt="Some caption"/>
            <figcaption>Some caption</figcaption>
        </div>
    """

    class ImageFigCaptionTreeprocessor(Treeprocessor):
        def run(self, root: etree.ElementTree) -> None:
            self.add_img_alt_as_figcaption(root)

        def add_img_alt_as_figcaption(self, element: etree.ElementTree) -> None:
            for container in element.iterfind("p"):
                assert container.tag == "p"
                image = container.find("img")
                if image is None:
                    continue
                assert image.tag == "img"
                self.append_figcaption(container, image)

        def append_figcaption(
            self, container: etree.Element, image: etree.Element
        ) -> None:
            alt = image.get("alt")

            if not alt:
                return

            # There's a weird bug that causes figcaption to appear *below*
            # the containing paragraph, instead of inside (alongside the image),
            # when using '.append()'.
            #
            # As a workaround, generate a new div, append it to the paragraph -- so that
            # it is actually *below* the paragraph (yup, hacky) -- and remove the
            # original image.

            div = etree.Element("div")
            div.set("class", "p-image")
            div.append(image)
            caption = etree.SubElement(div, "figcaption")
            caption.text = alt

            container.append(div)
            container.remove(image)

    def extendMarkdown(self, md: Markdown) -> None:
        md.treeprocessors.register(
            self.ImageFigCaptionTreeprocessor(md), "img_figcaption", 5
        )
