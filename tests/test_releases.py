from pageobjects.base import PageObject
from pageobjects.environments import RedhatAccountPopup
from pageobjects.header import Header
from pageobjects.releases import Releases
from settings import OPENSTACK_REDHAT
from tests.base import BaseTestCase


class TestReleases(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        BaseTestCase.setUpClass()

    def setUp(self):
        BaseTestCase.clear_nailgun_database()
        BaseTestCase.setUp(self)
        Header().releases.click()

    def test_rhsm(self):
        Releases().rhel_setup.click()
        with RedhatAccountPopup() as p:
            p.license_rhsm.click()
            p.redhat_username.send_keys('rheltest')
            p.redhat_password.send_keys('password')
            p.apply.click()
            p.wait_until_exists()
        with Releases() as r:
            PageObject.wait_until_exists(
                r.dict[OPENSTACK_REDHAT].download_progress, timeout=20)
            self.assertEqual(
                'Active', r.dict[OPENSTACK_REDHAT].status.text,
                'RHOS status is active')

    def test_rhn_satellite(self):
        Releases().rhel_setup.click()
        with RedhatAccountPopup() as p:
            p.license_rhn.click()
            p.redhat_username.send_keys('rheltest')
            p.redhat_password.send_keys('password')
            p.redhat_satellite.send_keys('satellite.example.com')
            p.redhat_activation_key.send_keys('1234567890')
            p.apply.click()
            p.wait_until_exists()
        with Releases() as r:
            PageObject.wait_until_exists(
                r.dict[OPENSTACK_REDHAT].download_progress, timeout=20)
            self.assertEqual(
                'Active', r.dict[OPENSTACK_REDHAT].status.text,
                'RHOS status is active')