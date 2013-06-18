from engine.poteen.elements.basic.htmlElement import HtmlElement
from .....components.functionality.cluster.generic.configure_view \
    import ConfigureView
from .....components.generic.abstractView import AbstractView


class ConfigureInterfaces(ConfigureView):

    def __init__(self):
        self.interface_box = HtmlElement(
            xpath=".//div[@class='physical-network-box' and "
                  "div[@class='network-box-name']='{name}']",
            element_name="Interface {name}")

        self.interface_drop_area = HtmlElement(
            xpath=".//div[@class='physical-network-box' and "
                  "div[@class='network-box-name']='{name}']//"
                  "div[contains(@class,'ui-sortable')]",
            element_name="Interface {name} drop area")

        self.network_item = HtmlElement(
            xpath=".//div[@class='logical-network-item' and "
                  "div[@class='name']='{name}']",
            element_name="Network item {name}")

        AbstractView.__init__(self)

    def drag_network_to(self, network, interface):
        network_element = self.network_item.find(name=network)
        interface_element = self.interface_drop_area.find(name=interface)
        self._action_bot._drag_and_drop(network_element.get_element(),
                                        interface_element.get_element())
