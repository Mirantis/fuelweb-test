from engine.poteen.elements.basic.button import Button
from tests.components.generic.abstractDialog import AbstractDialog


class ConfirmLeavePageDialog(AbstractDialog):

    def __init__(self):
        self.stay_on_page_btn = Button(
            xpath=".//button[@class='btn btn-return']",
            element_name="Stay on page button"
        )
        self.leave_page_discard_changes_button = Button(
            xpath=".//button[@class='btn btn-danger proceed-btn']",
            element_name="Leave page and discard changes button"
        )

    def click_stay_on_page(self):
        return self.stay_on_page_btn.click_and_wait()

    def click_leave_page(self):
        return self.leave_page_discard_changes_button.click_and_wait()
