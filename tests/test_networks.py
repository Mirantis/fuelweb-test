from pageobjects.environments import Environments, Wizard
from pageobjects.networks import Networks
from pageobjects.tabs import Tabs
from settings import *
from tests.base import BaseTestCase

RANGES = [
    ['192.16.0.2', '192.16.0.10'],
    ['192.168.10.20', '192.168.10.50']
]


class BaseClass(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()
        cls.get_home()
        Environments().create_cluster_box.click()
        with Wizard() as w:
            w.name.send_keys(OPENSTACK_CENTOS)
            w.release.select_by_visible_text(OPENSTACK_RELEASE_CENTOS)
            for i in range(6):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

    def setUp(self):
        BaseTestCase.setUp(self)
        Environments().create_cluster_boxes[0].click()
        Tabs().networks.click()

    def _test_ranges_plus_icon(self, network):
        with getattr(Networks(), network) as p:
            p.ip_ranges[0].icon_plus.click()
            self.assertEqual(len(p.ip_ranges), 2, 'Plus icon. row 1')
            p.ip_ranges[1].icon_plus.click()
            self.assertEqual(len(p.ip_ranges), 3, 'Plus icon. row 2')
            p.ip_ranges[1].start.send_keys(RANGES[0][0])
            p.ip_ranges[1].end.send_keys(RANGES[0][1])
            p.ip_ranges[0].icon_plus.click()
            self.assertEqual(len(p.ip_ranges), 4, 'Plus icon. row 1')
            self.assertEqual(p.ip_ranges[1].start.get_attribute('value'), '')
            self.assertEqual(p.ip_ranges[1].end.get_attribute('value'), '')
            self.assertEqual(p.ip_ranges[2].start.get_attribute('value'), RANGES[0][0])
            self.assertEqual(p.ip_ranges[2].end.get_attribute('value'), RANGES[0][1])

    def _test_ranges_minus_icon(self, network):
        with getattr(Networks(), network) as p:
            for i in range(3):
                p.ip_ranges[i].icon_plus.click()
            p.ip_ranges[3].icon_minus.click()
            self.assertEqual(len(p.ip_ranges), 3, 'Minus icon. last row')
            p.ip_ranges[2].start.send_keys(RANGES[0][0])
            p.ip_ranges[2].end.send_keys(RANGES[0][1])
            p.ip_ranges[1].icon_minus.click()
            self.assertEqual(len(p.ip_ranges), 2, 'Minus icon. second row')
            self.assertEqual(p.ip_ranges[1].start.get_attribute('value'), RANGES[0][0])
            self.assertEqual(p.ip_ranges[1].end.get_attribute('value'), RANGES[0][1])


class TestPublicNetwork(BaseClass):

    def test_ranges_plus_icon(self):
        self._test_ranges_plus_icon('public')

    def test_ranges_minus_icon(self):
        self._test_ranges_minus_icon('public')


class TestFloatingNetwork(BaseClass):

    def test_ranges_plus_icon(self):
        self._test_ranges_plus_icon('floating')

    def test_ranges_minus_icon(self):
        self._test_ranges_minus_icon('floating')
