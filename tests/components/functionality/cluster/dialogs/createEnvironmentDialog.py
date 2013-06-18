from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.input import Input
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.resultList import ResultList
from engine.poteen.utils.storage import Storage
from .....components.generic.abstractDialog import AbstractDialog
from .....testdata.cluster import TD_Cluster


class CreateEnvironmentDialog(AbstractDialog):
    def __init__(self):
        self.name = Input(
            xpath=".//input[@name='name']", element_name="Name"
        )
        self.nameErrorMessage = HtmlElement(
            xpath="//div[contains(@class,'control-group') and "
                  ".//input[contains(@name, 'name')]]"
                  "//span[@class='help-inline']",
            element_name="name error message"
        )
        self.version = Select(
            xpath=".//select[@name='release']", element_name="Version"
        )

        AbstractDialog.__init__(self)

    def populate(self, name, version, submit=False):
        environment = Storage.get_current(TD_Cluster.NAME)
        environment.name = name
        environment.version = version

        rl = ResultList("Populate create new Environment dialog") \
            .push(self.name.set_value(name)) \
            .push(self.version.set_value(version))
        if submit:
            rl.push(self.create())
        return rl

    def verify_name_error(self, value):
        return self.nameErrorMessage.verify_value(value)
