from engine.poteen.elements.basic.button import Button
from .....components.generic.abstractView import AbstractView


class ConfigureView(AbstractView):

    def __init__(self):
        self.cancelChanges = Button(
            xpath="//button[contains(@class, 'btn-revert-changes')]",
            element_name="Cancel Changes")

        self.loadDefaults = Button(
            xpath="//button[contains(@class, 'btn-defaults')]",
            element_name="Load Changes")

        self.backToNodeList = Button(
            xpath="//button[contains(@class, 'btn-return')]",
            element_name="Back To Node List")

        AbstractView.__init__(self)
