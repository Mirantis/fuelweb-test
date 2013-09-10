from engine.poteen.bots.verifyBot import VerifyBot
from engine.poteen.elements.basic.radio import Radio
from engine.poteen.log.resultList import ResultList
from .....components.generic.abstractDialog import AbstractDialog


class EnvironmentDeploymentModeDialog(AbstractDialog):
    deploymentMode = Radio(
        xpath=".//div[contains(@class, 'mode-control-group')]"
              "//label[div[contains(@class, 'parameter-name') "
              "and text()='{mode}']]",
        element_name="Deployment mode [{mode}]")

    deploymentType = Radio(
        xpath=".//div[contains(@class, 'type-control-group')]"
              "//label[div[contains(@class, 'parameter-name') "
              "and text()='{type}']]",
        element_name="Deployment type [{type}]")

    def __init__(self):
        AbstractDialog.__init__(self)

    def populate(self, deploymentMode, clickNext=False):
        rl = ResultList("Populate Environment mode")\
            .push(self.select_deployment_mode(deploymentMode))
        if clickNext:
            if VerifyBot().is_element_displayed(self.BUTTON_APPLY):
                rl.push(self.apply())
            else:
                rl.push(self.clickNext())
        return rl

    def select_deployment_mode(self, value):
        return self.deploymentMode.find(mode=value).click()

    def select_deployment_type(self, value):
        return self.deploymentType.find(type=value).click()
