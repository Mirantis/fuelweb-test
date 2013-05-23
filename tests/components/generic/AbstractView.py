from engine.poteen.BasePage import BasePage
from engine.poteen.elements.basic.Button import Button


class AbstractView(BasePage):
    applyButton = Button(xpath=".//div[contains(@class, 'btn-apply')]",
                         element_name="Apply")

    cancelButton = Button(xpath=".//div[contains(@class, 'btn-discard')]",
                          element_name="Cancel")

    def __init__(self, parent=None):
        BasePage.__init__(self, parent)

    def apply(self):
        return self.applyButton.click()

    def cancel(self):
        return self.cancelButton.click()