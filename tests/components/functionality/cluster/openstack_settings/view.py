from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.link import Link
from engine.poteen.elements.basic.radio import Radio
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.resultList import ResultList
from engine.poteen.log.result import Result
from ....generic.abstractView import AbstractView
from ..dialogs.environmentDeploymentModeDialog \
    import EnvironmentDeploymentModeDialog
from tests.components.functionality.cluster.generic.ip_range_row import IpRangeRow


class OpenstackSettingsView(AbstractView):
    def __init__(self, parent=None):
        self.parameter_input = Input(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]='{name}']//"
                  "input[@type='text']",
            element_name="Parameter {name}")

        self.parameter_radio = Input(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]='{name}']//"
                  "input[@type='radio']",
            element_name="Parameter {name}")

        self.parameter_checkbox = Input(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]='{name}']//"
                  "input[@type='checkbox']",
            element_name="Parameter {name}")

        AbstractView.__init__(self, parent)

    def set_parameter_input(self, name, value):
        return self.parameter_input.find(name=name).set_value(value)

    def set_parameter_radio(self, name, value):
        return self.parameter_radio.find(name=name).set_value(value)

    def set_parameter_checkbox(self, name, value):
        return self.parameter_checkbox.find(name=name).set_value(value)