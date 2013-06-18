from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.resultList import ResultList
from .....components.generic.abstractDialog import AbstractDialog


class NodeHardwareDialog(AbstractDialog):

    BUTTON_NETWORK_CONFIGURATION = "Network Configuration"
    BUTTON_DISK_CONFIGURATION = "Disk Configuration"

    def __init__(self):
        self.accordion_header = HtmlElement(
            xpath="//div[@class='accordion-toggle' "
            "and contains(text(),'{name}')]/p",
            element_name="Accordion header [{name}]")

        AbstractDialog.__init__(self)

    def click_memory(self):
        return self.accordion_header.find(name='memory')

    def click_interfaces(self):
        return self.accordion_header.find(name='interfaces')

    def click_disks(self):
        return self.accordion_header.find(name='disks')

    def click_system(self):
        return self.accordion_header.find(name='system')

    def click_cpu(self):
        return self.accordion_header.find(name='cpu')

    def click_network_configuration(self):
        return self.click_footer_button(self.BUTTON_NETWORK_CONFIGURATION)

    def click_disk_configuration(self):
        return self.click_footer_button(self.BUTTON_DISK_CONFIGURATION)
