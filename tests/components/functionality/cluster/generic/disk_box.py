from selenium.common.exceptions import ElementNotVisibleException
from engine.poteen.basePage import BasePage
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.resultList import ResultList
from .....components.functionality.cluster.generic.volume_group \
    import VolumeGroup
from .....components.functionality.cluster.generic.volume_group_box \
    import VolumeGroupBox


class DiskBox(BasePage):
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
            xpath=".//div[contains(@class,'disk-map-details-item')]",
            element_name="Disk parameter {name}")

        self.disk_map_details = HtmlElement(
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
            xpath=".//div[@class='disk-map-short disk-map-full']",
            element_name="Disk map")

        BasePage.__init__(self, parent)

    def get_volume_group(self, name):
        return VolumeGroup(self.volume_group.find(name=name).get_element())

    def get_volume_group_box(self, name):
        return VolumeGroupBox(self.volume_group_box.find(name=name))

    def click_disk_map(self):
        rl = ResultList("Click disk map")

        elements = self._parent\
            .find_elements_by_xpath(".//div[@class='toggle-volume']")
        for el in elements:
            try:
                res = HtmlElement(element=el).click()
                if not res.i_passed():
                    raise ElementNotVisibleException()
            except ElementNotVisibleException:
                continue
            else:
                break
        rl.push(res)

        WaitBot().wait_for_web_element_stop_resizing(
            self.disk_map.find().get_element())
        return rl

    def verify_volume_size_is_identical(self, name):
        rl = ResultList("Verify volume size is identical everywhere")
        group_box_size = self.get_volume_group_box(name).size.get_value()
        rl.push(self.get_volume_group(name).size.verify_value_contains(
            group_box_size))
        return rl
