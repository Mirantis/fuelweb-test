from engine.poteen.elements.basic.input import Input
from ....generic.abstractView import AbstractView


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
