from .....components.generic.abstractDialog import AbstractDialog
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement


class DeployChangesDialog(AbstractDialog):
    def __init__(self):
        AbstractDialog.__init__(self)
        self.disabled_deploy_btn = Button(
            xpath=".//button["
                  "contains(@class,'start-deployment-btn disabled')]",
            element_name="Disabled deploy button"
        )
        self.alert_message = HtmlElement(
            xpath=".//div[@class='alert alert-error']",
            element_name="Alert error message"
        )
