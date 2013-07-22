from selenium.webdriver.common.by import By
from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.elements.basic.radio import Radio as EngineRadio


class Radio(EngineRadio):
    def __init__(self, *args, **kwargs):
        EngineRadio.__init__(self, *args, **kwargs)
        self._type = "radiobutton"

    def get_value(self):
        element = ActionBot().find_element(By.TAG_NAME, "input", self.get_element())
        return self.VALUE_ON \
            if element.is_selected() \
            else self.VALUE_OFF
