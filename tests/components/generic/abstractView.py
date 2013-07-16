from engine.poteen.basePage import BasePage
from engine.poteen.elements.basic.button import Button


class AbstractView(BasePage):
    def __init__(self, parent=None):
        self.applyButton = Button(
            xpath=".//*[self::button or self::div]"
                  "[contains(@class, 'btn-apply')]",
            element_name="Apply"
        )
        self.cancelButton = Button(
            xpath=".//*[self::button or self::div]"
                  "[contains(@class, 'btn-discard')]",
            element_name="Cancel"
        )

        BasePage.__init__(self, parent)

    def apply(self):
        return self.applyButton.click()

    def cancel(self):
        return self.cancelButton.click_and_wait()
