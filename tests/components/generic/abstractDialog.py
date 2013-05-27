from selenium.webdriver.common.by import By
from engine.poteen.elements.basic.button import Button
from .abstractView import AbstractView


class AbstractDialog(AbstractView):
    XPATH_DIALOG = "/html/body/div[contains(@class,'modal ')]"

    BUTTON_APPLY = "Apply"
    BUTTON_CREATE = "Create"
    BUTTON_CANCEL = "Cancel"
    BUTTON_DELETE = "Delete"
    BUTTON_DEPLOY = "Deploy"

    elementClose = Button(
        xpath="./div[@class='modal-header']/button[@class='close']",
        element_name="Dialog [x] header icon")

    footerButton = Button(
        xpath="./div[@class='modal-footer']/button[contains(.,'{name}')]",
        element_name="Dialog footer button [{name}]")

    def __init__(self):
        self.wait_loading()
        AbstractView.__init__(self, self.__get_control_dialog())

    @classmethod
    def __get_control_dialog(cls):
        return cls.get_wait_bot().wait_for_web_element(
            By.XPATH, cls.XPATH_DIALOG)

    def apply(self):
        return self.click_footer_button(self.BUTTON_APPLY)

    def cancel(self):
        return self.click_footer_button(self.BUTTON_CANCEL)

    def click_footer_button(self, name):
        res = self.footerButton.find(name=name).click_and_wait()
        self.wait_closing()
        return res

    def close(self):
        return self.elementClose.click_and_wait()

    def create(self):
        return self.click_footer_button(self.BUTTON_CREATE)

    def delete(self):
        return self.click_footer_button(self.BUTTON_DELETE)

    def deploy(self):
        return self.click_footer_button(self.BUTTON_DEPLOY)

    def wait_closing(self):
        self.get_wait_bot().wait_for_disappears(By.XPATH, self.XPATH_DIALOG)
        self.get_wait_bot().wait_loading()

    def wait_loading(self):
        self.get_wait_bot().wait_for_stop_moving(By.XPATH, self.XPATH_DIALOG)
        self.get_wait_bot().wait_loading()

