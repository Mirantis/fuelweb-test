from pageobjects.environments import Environments, Wizard
from settings import *
from tests.base import BaseTestCase


class Environment:

    @staticmethod
    def simple_flat(name=OPENSTACK_CENTOS,
                    release=OPENSTACK_RELEASE_CENTOS):
        BaseTestCase.get_home()
        Environments().create_cluster_box.click()
        with Wizard() as w:
            w.name.send_keys(name)
            w.release.select_by_visible_text(release)
            for i in range(6):
                w.next.click()
            w.create.click()
            w.wait_until_exists()

    @staticmethod
    def simple_neutron_gre(name=OPENSTACK_CENTOS,
                           release=OPENSTACK_RELEASE_CENTOS):
        BaseTestCase.get_home()
        Environments().create_cluster_box.click()
        with Wizard() as w:
            w.name.send_keys(name)
            w.release.select_by_visible_text(release)
            for i in range(3):
                w.next.click()
            w.network_neutron_gre.click()
            for i in range(3):
                w.next.click()
            w.create.click()
            w.wait_until_exists()