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
        self.checkbox_controller = Checkbox(
            xpath=".//input[@type='checkbox' and @value='controller']",
            element_name="Checkbox controller"
        )
        self.checkbox_compute = Checkbox(
            xpath=".//input[@type='checkbox' and @value='compute']",
            element_name="Checkbox compute"
        )
        self.checkbox_cinder = Checkbox(
            xpath=".//input[@type='checkbox' and @value='cinder']",
            element_name="Checkbox cinder"
        )
        self.assign = Button(
            xpath=".//button[@class='btn btn-success btn-assign']",
            element_name="Assign button"
        )
        self.conflict_controller = HtmlElement(
            xpath="role-conflict controller",
            element_name="Conflict controller"
        )
        self.conflict_compute = HtmlElement(
            xpath="role-conflict compute",
            element_name="Conflict compute"
        )
        self.conflict_cinder = HtmlElement(
            xpath="role-conflict cinder",
            element_name="Conflict cinder"
        )
        AbstractView.__init__(self, parent)
