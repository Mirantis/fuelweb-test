from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.checkbox import Checkbox
from engine.poteen.elements.basic.input import Input
from ....generic.abstractView import AbstractView
from tests.components.elements.Radio import Radio


class OpenstackSettingsView(AbstractView):
    def __init__(self, parent=None):
        self.save_settings = Button(
            xpath=".//button[contains(@class, 'btn-apply-changes')]",
            element_name="Save Settings")

        self.cancel_changes = Button(
            xpath=".//button[contains(@class, 'btn-revert-changes')]",
            element_name="Cancel Changes")

        self.load_defaults = Button(
            xpath=".//button[contains(@class, 'btn btn-load-defaults')]",
            element_name="Load Defaults")

        self.parameter_input = Input(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]='{name}']//"
                  "input[@type='text']",
            element_name="Parameter {name}")

        self.parameter_radio = Radio(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]='{name}']",
            element_name="Parameter {name}")

        self.parameter_checkbox = Checkbox(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]='{name}']//"
                  "input[@type='checkbox']",
            element_name="Parameter {name}")

        self.show_password = Button(
            xpath=".//span[@class='add-on' "
                  "and i[contains(@class, 'icon-eye')]]",
            element_name="Show password button")

        self.show_password_on = Button(
            xpath=".//i[@class ='icon-eye' and @style='display: inline;']",
            element_name="Show password button")

        self.show_password_off = Button(
            xpath=".//i[@class ='icon-eye-off hide' "
                  "and @style='display: inline;']",
            element_name="Show password button")

        AbstractView.__init__(self, parent)

    def set_parameter_input(self, name, value):
        return self.parameter_input.find(name=name).set_value(value)

    def set_parameter_radio(self, name, value):
        return self.parameter_radio.find(name=name).set_value(value)

    def set_parameter_checkbox(self, name, value):
        return self.parameter_checkbox.find(name=name).set_value(value)

    def verify_parameter_input(self, name, value):
        return self.parameter_input.find(name=name).verify_value(value)
