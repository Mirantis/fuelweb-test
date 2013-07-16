from engine.poteen.basePage import BasePage
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.input import Input

from engine.poteen.log.resultList import ResultList

class IpRangeRow(BasePage):
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

        BasePage.__init__(self, parent)

    def set_start_ip(self, args):
        return self.ip_range_start.set_value(args)

    def is_invalid(self):
        return self.ip_range_start.verify_attribute("class", "error")

    def is_correct(self):
        return self.ip_range_start.verify_attribute("class", "")

    def set_start_ip_verify_error(self, args):
        rl = ResultList("Set ip range start with '{args}' "
                        "and verify error".format(args=args)) \
            .push(self.set_start_ip(args)) \
            .push(self.is_invalid())
        return rl

    def set_start_ip_correct(self, args):
        rl = ResultList("Set ip range start with '{args}' and verify "
                        "error does not exist".format(args=args)) \
            .push(self.set_start_ip(args)) \
            .push(self.is_correct())
        return rl

    def set_start_ip_and_verify(self, args, value):
        if value:
            return self.set_start_ip_correct(args)
        else:
            return self.set_start_ip_verify_error(args)
