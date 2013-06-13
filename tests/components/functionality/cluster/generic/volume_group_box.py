from engine.poteen.elements.baseElement import BaseElement
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.link import Link


class VolumeGroupBox(BaseElement):
    def __init__(self, parent=None):
        self.name = HtmlElement(
            xpath=".//div[@class='volume-group-box-name']",
            element_name="name")

        self.size = Input(
            xpath=".//div[@class='volume-group-box-input']/input",
            element_name="size")

        self.use_all_unallocated = Link(
            xpath=".//div[@class='use-all-unallocated']",
            element_name="Use all unallocated")

        BaseElement.__init__(self, parent)
