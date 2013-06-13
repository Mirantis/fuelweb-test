from engine.poteen.elements.baseElement import BaseElement
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView
from tests.components.functionality.cluster.generic.volume_group import VolumeGroup
from tests.components.functionality.cluster.generic.volume_group_box import VolumeGroupBox


class IpRangeRow(BaseElement):
    def __init__(self, parent=None):
        self.ip_range_start = Input(
            xpath=".//input[@name='ip_ranges-start']",
            element_name="Ip range start")

        self.ip_range_end = Input(
            xpath=".//input[@name='ip_ranges-end']",
            element_name="Ip range end")

        self.ip_range_add = Button(
            xpath=".//button[contains(@class,'ip-ranges-add')]",
            element_name="Ip range add")

        self.ip_range_delete = Button(
            xpath=".//button[contains(@class,'ip-ranges-delete')]",
            element_name="Ip range delete")

        BaseElement.__init__(self, parent)
