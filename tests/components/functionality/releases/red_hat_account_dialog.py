from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.radio import Radio
from ....components.generic.abstractDialog import AbstractDialog


class RedHatAccountDialog(AbstractDialog):
    BUTTON_DOWNLOAD = "Download"

    def __init__(self):
        self.license_type = Radio(
            xpath='.//div[@class="custom-tumbler" '
                  'and input[@type="radio" and @value="{value}"]]',
            element_name="License type"
        )

        self.red_hat_username = Input(
            xpath='.//input[@name="username"]',
            element_name="Red Hat username"
        )

        self.red_hat_password = Input(
            xpath='.//input[@name="password"]',
            element_name="Red Hat password"
        )

        self.satellite_server_hostname = Input(
            xpath='.//input[@name="satellite"]',
            element_name="Satellite server hostname"
        )

        self.activation_key = Input(
            xpath='.//input[@name="activation_key"]',
            element_name="Activation key"
        )

        self.inline_help = HtmlElement(
            xpath='.//span[@class="help-inline" and contains(text(), "{}")]',
            element_name="Alert error"
        )

        AbstractDialog.__init__(self)

    def set_license_type(self, name, value):
        return self.license_type.find(value=name).set_value(value)

    def download(self):
        return self.click_footer_button(self.BUTTON_DOWNLOAD)
