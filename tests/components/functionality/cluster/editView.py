from selenium.webdriver.common.by import By
from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result
from engine.poteen.log.resultList import ResultList
from ...generic.abstractView import AbstractView


class Cluster_View(AbstractView):
    def __init__(self, parent=None):
        self.tab = HtmlElement(
            xpath="//div[@id='content']//ul[contains(@class, 'nav nav-tabs')]"
                  "/li[.//b[@class='{}']]",
            element_name="Tab"
        )
        self.deployChanges = Button(
            xpath="//button[contains(@class, 'deploy-btn')]",
            element_name="Deploy Changes"
        )
        self.deploymentBar = HtmlElement(
            xpath="//li[contains(@class, 'deployment-control')]"
                  "//div[contains(@class, 'progress-deploy')]",
            element_name="Deployment progress")

        self.successMessage = HtmlElement(
            xpath="//div[contains(@class, 'global-success')]/p",
            element_name="Success message"
        )

        self.errorMessage = HtmlElement(
            xpath="//div[contains(@class, 'global-error')]/p",
            element_name="Error message"
        )

        AbstractView.__init__(self, parent)

    def click_actions_tab(self):
        return ResultList("Click actions tab") \
            .push(self.tab.find("tab-actions-normal").click())

    def click_deploy_changes(self):
        return self.deployChanges.click()

    def wait_deployment_done(self, seconds, poll_frequency=5):
        return Result(
            "Wait for deployment done ({})".format(seconds),
            WaitBot(seconds).wait_for_disappears(
                By.XPATH,
                "//li[contains(@class, 'deployment-control')]"
                "//div[contains(@class, 'progress-deploy')] ",
                poll_frequency=poll_frequency
            )
        )

    def verify_success_message(self, value):
        return self.successMessage.verify_value_contains(value)

    def verify_error_message(self, value):
        return self.errorMessage.verify_value_contains(value)
