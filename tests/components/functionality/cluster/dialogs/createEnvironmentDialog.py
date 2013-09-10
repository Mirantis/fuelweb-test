from selenium.webdriver.common.by import By
from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.resultList import ResultList
from engine.poteen.utils.storage import Storage
from .....components.generic.abstractDialog import AbstractDialog
from .....testdata.cluster import TD_Cluster
from .....components.elements.Radio import Radio
from .environmentDeploymentModeDialog import EnvironmentDeploymentModeDialog
from ...cluster.openstack_settings.view import OpenstackSettingsView


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
        self.downloadType = Radio(
            xpath=".//div[contains(@class, 'custom-tumbler') "
                  "and input[@type='radio' and @value='{type}']]",
            element_name="Download type [{type}]")

        self.username = Input(
            xpath=".//input[@name='username']",
            element_name="Username"
        )
        self.password = Input(
            xpath=".//input[@name='password']",
            element_name="Password"
        )
        self.serverHostname = Input(
            xpath=".//input[@name='satellite']",
            element_name="Satellite server hostname"
        )
        self.activationKey = Input(
            xpath=".//input[@name='activation_key']",
            element_name="Activation key"
        )
        self.instruction = HtmlElement(
            xpath=".//div[@class='alert alert-info rhel-license hide']",
            element_name="Instruction to deploy RHOS"
        )
        self.releaseDescription = HtmlElement(
            xpath=".//div[@class='release-description help-block']",
            element_name="Release description"
        )
        self.message4thStep = HtmlElement(
            xpath=".//div[contains(text(), 'Configuration is finished and "
                  "now you can create your cluster!')]",
            element_name="Message: ready to create environment"
        )

        AbstractDialog.__init__(self)

    def populate(self, name, version, clickNext=False):
        environment = Storage.get_current(TD_Cluster.NAME)
        environment.name = name
        environment.version = version

        rl = ResultList("Populate create new Environment dialog") \
            .push(self.name.set_value(name)) \
            .push(WaitBot().wait_loading()) \
            .push(self.version.set_value(version)) \
            .push(self.name.click())
        if clickNext:
            WaitBot().wait_loading()
            WaitBot().wait_for_stop_resizing(By.XPATH, self.XPATH_DIALOG)
            rl.push(self.clickNext())
            WaitBot().wait_loading()
        return rl

    def verify_name_error(self, value):
        return self.nameErrorMessage.verify_value(value)

    def verify_release_description(self, value):
        return self.releaseDescription.verify_value_contains(value)

    def select_download_mode(self, value):
        return self.downloadType.find(type=value).set_value("on")

    def populateRHOS(self, name, version, downloadMode, username, password,
                     serverHostName, activationKey, clickNext=False):
        rl = ResultList("Populate new environment dialog with RHOS") \
            .push(self.populate(name, version))
        WaitBot().wait_loading()
        WaitBot().wait_for_stop_resizing(By.XPATH, self.XPATH_DIALOG)
        if VerifyBot().verify_visibility(self.instruction.get_element(),
                                         True, "instruction").i_passed():
            rl.push(self.select_download_mode(downloadMode))
            rl.push(self.username.set_value(username))
            rl.push(self.password.set_value(password))
            if downloadMode == 'rhn':
                rl.push(self.serverHostname.set_value(serverHostName))
                rl.push(self.activationKey.set_value(activationKey))
        if clickNext:
            WaitBot().wait_loading()
            WaitBot().wait_for_stop_resizing(By.XPATH, self.XPATH_DIALOG)
            rl.push(self.clickNext())
            WaitBot().wait_loading()
        return rl

    def create_environment(self, name, version, deploymentMode, computeType):
        rl = ResultList("Create new environment") \
            .push(self.populate(name, version, True))
        rl.push(EnvironmentDeploymentModeDialog().populate(
            deploymentMode, True))
        rl.push(OpenstackSettingsView().set_parameter_radio(
            computeType, "on"))
        rl.push(self.clickNext())
        rl.push(VerifyBot().verify_visibility(
            self.message4thStep.get_element(), True,
            "Message: ready to create environment"))
        rl.push(self.create())
        return rl

    def create_environment_RHOS(self, name, version, downloadMode, username,
                                password, serverHostName, activationKey,
                                deploymentMode, computeType):
        rl = ResultList("Create new environment") \
            .push(self.populateRHOS(name, version, downloadMode, username,
                                    password, serverHostName, activationKey,
                                    True))
        rl.push(EnvironmentDeploymentModeDialog().populate(
            deploymentMode, True))
        rl.push(OpenstackSettingsView().set_parameter_radio(
            computeType, "on"))
        rl.push(self.clickNext())
        rl.push(VerifyBot().verify_visibility(
            self.message4thStep.get_element(), True,
            "Message: ready to create environment"))
        rl.push(self.create())
        return rl
