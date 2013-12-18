import base64
from io import BytesIO
from unittest import TestCase
from PIL import Image
import operator
import math
import browser
from settings import *


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        browser.start_driver()
        cls.clear_nailgun_database()

    @classmethod
    def tearDownClass(cls):
        browser.quit_driver()

    def setUp(self):
        browser.driver.get('http://localhost:8000/')

    @staticmethod
    def clear_nailgun_database():
        from nailgun.db import dropdb
        from nailgun.db import syncdb
        from nailgun.db.sqlalchemy import fixman
        dropdb()
        syncdb()
        fixman.upload_fixtures()
        for fixture in NAILGUN_FIXTURES.split(':'):
            if fixture == '':
                continue
            with open(fixture, "r") as fileobj:
                fixman.upload_fixture(fileobj)

    def assert_screen(self, name):
        img_exp = Image.open('{}/{}.png'.format(FOLDER_SCREEN_EXPECTED, name))

        img_cur_base64 = browser.driver.get_screenshot_as_base64()
        img_cur = Image.open(BytesIO(base64.decodestring(img_cur_base64)))
        img_cur.save('{}/{}.png'.format(FOLDER_SCREEN_CURRENT, name))

        h1 = img_exp.histogram()
        h2 = img_cur.histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a-b)**2, h1, h2))/len(h1))

        self.assertNotEqual(rms == 0, 'Screen valid')
