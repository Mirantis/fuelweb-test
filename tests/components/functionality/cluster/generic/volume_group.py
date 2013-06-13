from engine.poteen.elements.baseElement import BaseElement
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.link import Link


class VolumeGroup(BaseElement):
    def __init__(self, parent=None):
        self.name = HtmlElement(
            xpath=".//div[@class='volume-group-name']",
            element_name="name")

        self.size = HtmlElement(
            xpath=".//div[@class='volume-group-size']",
            element_name="name")

        self.close = Link(
            xpath=".//div[@class='close-btn']",
            element_name="close")

        BaseElement.__init__(self, parent)
