from selenium.webdriver.common.by import By
from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.radio import Radio
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.resultList import ResultList
from engine.poteen.utils.storage import Storage
from .....components.generic.abstractDialog import AbstractDialog
from .....testdata.cluster import TD_Cluster


class CreateEnvironmentDialog(AbstractDialog):
    def __init__(self):
        self.name = Input(
            xpath=".//input[@name='name']", element_name="Name"
        )
        self.nameErrorMessage = HtmlElement(
            xpath="//div[contains(@class,'control-group') and "
                  ".//input[contains(@name, 'name')]]"
                  "//span[@class='help-inline']",
            element_name="name error message"
        )
        self.version = Select(
            xpath=".//select[@name='release']", element_name="Version"
        )

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

        self.alert_error = HtmlElement(
            xpath='.//div[contains(@class,"alert alert-error")]',
            element_name="Alert error"
        )

        AbstractDialog.__init__(self)

    def populate(self, name, version, submit=False):
        environment = Storage.get_current(TD_Cluster.NAME)
        environment.name = name
        environment.version = version

        rl = ResultList("Populate create new Environment dialog") \
            .push(self.name.set_value(name)) \
            .push(WaitBot().wait_loading())\
            .push(self.version.set_value(version))\
            .push(self.name.click())
        if submit:
            WaitBot().wait_loading()
            WaitBot().wait_for_stop_resizing(By.XPATH, self.XPATH_DIALOG)
            rl.push(self.create())
            WaitBot().wait_loading()
        return rl

    def verify_name_error(self, value):
        return self.nameErrorMessage.verify_value(value)

    def verify_releases_list(self, expected_releases):
        rl = ResultList("Verify releases list")
        web_elements_releases = ActionBot().find_elements(
            By.TAG_NAME, 'option', self.version.get_element())
        releases = [we.text for we in web_elements_releases]
        VerifyBot().verify_equal(set(expected_releases), set(releases), 'Releases')
        return  rl

    def set_license_type(self, name, value):
        return self.license_type.find(value=name).set_value(value)
