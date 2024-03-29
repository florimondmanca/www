from xml.etree import ElementTree as etree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ImageExtension(Extension):
    """
    A Python-Markdown extension that improves the rendering of images.

    Example
    -------

    Input:
        ![Some caption](path/to/image.png))

    Output:
        <div class="p-markdown-image">
            <img src="/path/to/mage.png" alt="Some caption" loading="lazy"/>
            <figcaption>Some caption</figcaption>
        </div>
    """

    class ImageTreeprocessor(Treeprocessor):
        def run(self, root: etree.Element) -> etree.Element | None:
            self._process_images(root)
            return None

        def _process_images(self, element: etree.Element) -> None:
            for container in element.iterfind("p"):
                assert container.tag == "p"
                image = container.find("img")
                if image is None:
                    continue
                assert image.tag == "img"
                self._process_image(container, image)

        def _process_image(
            self, container: etree.Element, image: etree.Element
        ) -> None:
            image.set("loading", "lazy")

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

            figure = etree.Element("figure")
            figure.set("class", "f-image")
            figure.append(image)
            caption = etree.SubElement(figure, "figcaption")
            caption.text = alt

            container.append(figure)
            container.remove(image)

    def extendMarkdown(self, md: Markdown) -> None:
        md.treeprocessors.register(self.ImageTreeprocessor(md), "www_image", 5)
