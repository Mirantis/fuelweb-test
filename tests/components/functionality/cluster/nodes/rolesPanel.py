from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.checkbox import Checkbox
from engine.poteen.elements.basic.htmlElement import HtmlElement
from ....generic.abstractView import AbstractView


class RolesPanel(AbstractView):

    def __init__(self, parent=None):
        self.checkbox_role = Checkbox(
            xpath="//input[@type='checkbox' and @value='{role}']",
            element_name="Checkbox '{role}'"
        )
        self.assign = Button(
            xpath=".//button[@class='btn btn-success btn-assign']",
            element_name="Assign button"
        )
        self.conflict_role = HtmlElement(
            xpath=".//div[@class='role-conflict '{role}'']",
            element_name="Conflict '{role}'"
        )
        AbstractView.__init__(self, parent)
