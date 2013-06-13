from engine.poteen.elements.baseElement import BaseElement
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView
from tests.components.functionality.cluster.generic.volume_group \
    import VolumeGroup
from tests.components.functionality.cluster.generic.volume_group_box \
    import VolumeGroupBox


class DiskBox(BaseElement):
    def __init__(self, parent=None):
        self.caption = HtmlElement(
            xpath=".//div[contains(@class,'disk-box-name')]",
            element_name="Caption")

        self.total_space = HtmlElement(
            xpath=".//div[contains(@class,'disk-box-size')]",
            element_name="Total space")

        self.bootable_marker = HtmlElement(
            xpath=".//div[contains(@class,'disk-box-name')]/span",
            element_name="Disk's bootable marker")

        self.volume_group = HtmlElement(
            xpath=".//div[contains(@class,'volume-group') and "
                  ".//div[@class='volume-group-name']='{name}']",
            element_name="Volume group {name}")

        self.disk_parameter = HtmlElement(
            xpath=".//div[contains(@class,'disk-map-details-item') and "
                  "div[@class='disk-map-details-name']='{name}']/"
                  "div[@class='disk-map-details-parameter']",
            element_name="Disk parameter {name}")

        self.volume_group_box = HtmlElement(
            xpath=".//div[contains(@class,'volume-group-box') and "
                  "div[@class='volume-group-box-name']='{name}']",
            element_name="Volume group box {name}")

        self.make_bootable = Button(
            xpath=".//button[text()='Make Bootable']",
            element_name="Make Bootable")

        self.disk_map = HtmlElement(
            xpath=".//div[@class='disk-map-short disk-map-full')]",
            element_name="Disk map")

        BaseElement.__init__(self, parent)

    def get_volume_group(self, name):
        return VolumeGroup(self.volume_group.find(name=name))

    def get_volume_group_box(self, name):
        return VolumeGroupBox(self.volume_group_box.find(name=name))
