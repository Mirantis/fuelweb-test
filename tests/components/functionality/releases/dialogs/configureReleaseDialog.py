from .....components.generic.abstractDialog import AbstractDialog
from engine.poteen.elements.basic.input import Input
from engine.poteen.log.resultList import ResultList
from tests.components.elements.Radio import Radio


class Configure_Release_Dialog(AbstractDialog):
    def __init__(self):
        self.licence_rhsm = Radio(
            xpath=".//div[@class='custom-tumbler' "
                  "and input[@value='rhsm']]",
            element_name="RHSM"
        )
        self.licence_rhn = Radio(
            xpath=".//div[@class='custom-tumbler' "
                  "and input[@value='rhn']]",
            element_name="RHN Satellite"
        )
        self.rh_user = Input(
            xpath=".//input[@name='username']",
            element_name="Red Hat Username"
        )
        self.rh_password = Input(
            xpath=".//input[@name='password']",
            element_name="Red Hat Password"
        )
        self.satellite_server = Input(
            xpath=".//input[@name='satellite']",
            element_name="Satellite server hostname"
        )
        self.activation_key = Input(
            xpath=".//input[@name='activation_key']",
            element_name="Activation key"
        )
        AbstractDialog.__init__(self)

    def download(self):
        return self.footerButton.find(name="Download").click()

    def populate(self, name, password, server=None, key=None):
        rl = ResultList("Populate dialog")\
            .push(self.rh_user.set_value(name))\
            .push(self.rh_password.set_value(password))
        if server is not None:
            rl.push(self.satellite_server.set_value(server))\
                .push(self.activation_key.set_value(key))
        return rl

    def verify_controls_presence(self, licence):
        rl = ResultList(
            "Verify controls presence on form for {}".format(licence)
        )
        if licence == "RHSM":
            rl.push(self.rh_user.verify_visible(True)) \
                .push(self.rh_password.verify_visible(True)) \
                .push(self.satellite_server.verify_visible(False)) \
                .push(self.activation_key.verify_visible(False))
        else:
            rl.push(self.rh_user.verify_visible(True)) \
                .push(self.rh_password.verify_visible(True)) \
                .push(self.satellite_server.verify_visible(True)) \
                .push(self.activation_key.verify_visible(True))
        return rl
