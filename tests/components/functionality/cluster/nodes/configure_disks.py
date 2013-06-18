from engine.poteen.elements.basic.htmlElement import HtmlElement
from .....components.functionality.cluster.generic.configure_view \
    import ConfigureView
from .....components.functionality.cluster.generic.disk_box import DiskBox
from .....components.generic.abstractView import AbstractView


class ConfigureDisks(ConfigureView):

    def __init__(self):
        self.disk_box = HtmlElement(
            xpath=".//div[@class='disk-box disk' and "
                  "contains(div[@class='disk-box-name pull-left'],'{name}')]",
            element_name="Disk box {name}")

        AbstractView.__init__(self)

    def get_disk_box(self, name):
        return DiskBox(self.disk_box.find(name=name).get_element())
