from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.checkbox import Checkbox
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.resultList import ResultList

from .....components.generic.abstractDialog import AbstractDialog
from .....components.elements.Radio import Radio
from engine.poteen.utils.storage import Storage
from tests.testdata.cluster import TD_Cluster


class CreateEnvironmentDialog(AbstractDialog):

    def __init__(self):

        self.activationKey = Input(
            xpath=".//input[@name='activation_key']",
            element_name="Activation key"
        )
        self.deploymentMode = Radio(
            xpath=".//div[contains(@class, 'mode-control-group')]"
            "//label[div[contains(@class, 'parameter-name') "
            "and text()='{mode}']]",
            element_name="Deployment mode [{mode}]"
        )
        self.downloadType = Radio(
            xpath=".//div[contains(@class, 'custom-tumbler') "
                  "and input[@type='radio' and @value='{type}']]",
            element_name="Download type [{type}]"
        )
        self.instruction = HtmlElement(
            xpath=".//div[@class='alert alert-info rhel-license hide']",
            element_name="Instruction to deploy RHOS"
        )
        self.message_configuration_ready = HtmlElement(
            xpath=".//div[contains(text(), 'Configuration is finished and "
                  "now you can create your cluster!')]",
            element_name="Message: ready to create environment"
        )
        self.name = Input(
            xpath=".//input[@name='name']", element_name="Name"
        )
        self.nameErrorMessage = HtmlElement(
            xpath="//div[contains(@class,'control-group') and "
                  ".//input[contains(@name, 'name')]]"
                  "//span[@class='help-inline']",
            element_name="name error message"
        )
        self.parameter_radio = Radio(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]/text()='{name}']",
            element_name="Parameter {name}"
        )
        self.parameter_checkbox = Checkbox(
            xpath=".//label[contains(@class,'parameter-box') and "
                  "div[contains(@class,'parameter-name')]='{name}']//"
                  "input[@type='checkbox']",
            element_name="Parameter {name}")
        self.password = Input(
            xpath=".//input[@name='password']",
            element_name="Password"
        )
        self.releaseDescription = HtmlElement(
            xpath=".//div[@class='release-description help-block']",
            element_name="Release description"
        )
        self.serverHostname = Input(
            xpath=".//input[@name='satellite']",
            element_name="Satellite server hostname"
        )
        self.storage_cinder = Radio(
            xpath=".//div[contains(@class, 'span6') and contains(./h5/text(), "
                  "'Cinder backend')]//label[contains(@class,'parameter-box') "
                  "and div[contains(@class,'parameter-name')]"
                  "/text()='{name}']",
            element_name="Cinder backend {name}"
        )
        self.storage_glance = Radio(
            xpath=".//div[contains(@class, 'span6') and contains(./h5/text(), "
                  "'Glance backend')]//label[contains(@class,'parameter-box') "
                  "and div[contains(@class,'parameter-name')]"
                  "/text()='{name}']",
            element_name="Glance backend {name}"
        )
        self.username = Input(
            xpath=".//input[@name='username']",
            element_name="Username"
        )
        self.version = Select(
            xpath=".//select[@name='release']", element_name="Version"
        )

        AbstractDialog.__init__(self)

    def select_deployment_mode(self, value):
        return self.deploymentMode.find(mode=value).click()

    def populate(self, settings, clickNext=False):
        environment = Storage.get_current(TD_Cluster.NAME)
        environment.name = settings["name"]
        environment.version = settings["version"]

        rl = ResultList("Populate create new Environment dialog")

        rl.push(self.name.set_value(settings["name"]))
        rl.push(WaitBot().wait_loading())
        rl.push(self.version.set_value(settings["version"]))
        rl.push(self.name.click())

        if "rh" in settings and len(settings["rh"]) > 0 and \
                self.instruction.is_visible():

            rh = settings["rh"]
            self.wait_loading()
            rl.push(self.select_download_mode(rh["mode"]))
            rl.push(self.username.set_value(rh["username"]))
            rl.push(self.password.set_value(rh["password"]))

            if rh["mode"] == 'rhn':
                rl.push(self.serverHostname.set_value(rh["host"]))
                rl.push(self.activationKey.set_value(rh["activation_key"]))

        if clickNext:
            self.wait_loading()
            rl.push(self.clickNext())
            WaitBot().wait_loading()

        return rl

    def verify_name_error(self, value):
        return self.nameErrorMessage.verify_value(value)

    def verify_release_description(self, value):
        return self.releaseDescription.verify_value_contains(value)

    def select_download_mode(self, value):
        return self.downloadType.find(type=value).set_value("on")

    def set_parameter_radio(self, name, value):
        return self.parameter_radio.find(name=name).set_value(value)

    def set_parameter_checkbox(self, name, value):
        return self.parameter_checkbox.find(name=name).set_value(value)

    def create_environment(self, settings):
        """
        :param settings: {
            "name": "",
            "version": "",
            "rh": {
                "mode": "",
                "username": "",
                "password": "",
                "host": "",
                "activation_key": ""
            },
            "deployment_mode": "",
            "compute_type": "",
            "network": "",
            "storage": {
                "cinder": "",
                "glance": ""
            },
            "services":{
                "savanna": True,
                "murano": True
            }
        }
        """
        rl = ResultList("Create new environment")

        rl.push(self.populate(settings, True))

        rl.push(self.select_deployment_mode(settings["deployment_mode"]))
        rl.push(self.clickNext(()))

        #Set compute type (hypervisor)
        if "compute_type" in settings:
            rl.push(self.set_parameter_radio(
                settings["compute_type"], Radio.VALUE_ON))
        rl.push(self.clickNext())

        # Set network type
        if "network" in settings:
            rl.push(self.set_parameter_radio(
                settings["network"], Radio.VALUE_ON))
        rl.push(self.clickNext())

        if "storage" in settings:
            storage = settings["storage"]
            # Set cinder backend
            if "cinder" in storage:
                rl.push(
                    self.storage_cinder.find(storage["cinder"])
                    .set_value(Radio.VALUE_ON))

            # Set glance backend
            if "glance" in storage:
                rl.push(
                    self.storage_glance.find(storage["glance"])
                    .set_value(Radio.VALUE_ON))
        rl.push(self.clickNext())

        if "services" in settings:
            services = settings["services"]
            if "savanna" in services and services["savanna"]:
                rl.push(self.set_parameter_checkbox(
                    "Install Savanna", Checkbox.VALUE_ON))
            if "murano" in services and services["murano"]:
                rl.push(self.set_parameter_checkbox(
                    "Install Murano", Checkbox.VALUE_ON))
        rl.push(self.clickNext())

        rl.push(self.create())
        return rl
