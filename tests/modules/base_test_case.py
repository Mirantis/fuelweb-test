
from engine.poteen.testCasePoteen import TestCasePoteen
from ..ci.ci_fuel_web import CiFuelWeb


class BaseTestCase(TestCasePoteen):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.ci().get_empty_state()

    def ci(self):
        if not hasattr(self, '_ci'):
            self._ci = CiFuelWeb()
        return self._ci