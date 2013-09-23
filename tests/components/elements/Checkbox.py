from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.elements.basic.checkbox import Checkbox as EngineCheckbox
from engine.poteen.log.result import Result
from engine.poteen.log.resultList import ResultList


class Checkbox(EngineCheckbox):
    def __init__(self, *args, **kwargs):
        EngineCheckbox.__init__(self, *args, **kwargs)
        self._type = "checkbox"

    def set_value(self, value):
        value = self.__check_value(value)

        res = ResultList("Set checkbox [{}] to: [{}]".format(
            self._element_name, value
        ))
        if not self.get_value() == value:
            res.push(ActionBot().click(
                self.get_element(), self._element_name, self._type, True))
        else:
            res.push(
                Result(
                    "The checkbox [{}] already set to: [{}]".format(
                        self._element_name,
                        value
                    )
                )
            )
        return res
