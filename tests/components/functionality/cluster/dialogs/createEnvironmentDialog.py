from selenium.webdriver.common.by import By
from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.resultList import ResultList
from engine.poteen.utils.storage import Storage
from .....components.generic.abstractDialog import AbstractDialog
from .....testdata.cluster import TD_Cluster
from tests.components.functionality.releases.red_hat_account_dialog \
    import RedHatAccountDialog


class CreateEnvironmentDialog(AbstractDialog, RedHatAccountDialog):
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

        AbstractDialog.__init__(self)
        RedHatAccountDialog.__init__(self)

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
        VerifyBot().verify_equal(
            set(expected_releases), set(releases), 'Releases')
        return rl
