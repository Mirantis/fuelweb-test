import base64
from io import BytesIO
from unittest import TestCase
from PIL import Image
import operator
import math
from fuelui_tests import browser
from fuelui_tests.settings import *


class BaseTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        browser.start_driver()

    @classmethod
    def tearDownClass(cls):
        browser.quit_driver()

    def setUp(self):
        browser.driver.get('http://localhost:8000/')

    def assert_screen(self, name):
        img_exp = Image.open('{}/{}.png'.format(FOLDER_SCREEN_EXPECTED, name))

        img_cur_base64 = browser.driver.get_screenshot_as_base64()
        img_cur = Image.open(BytesIO(base64.decodestring(img_cur_base64)))
        img_cur.save('{}/{}.png'.format(FOLDER_SCREEN_CURRENT, name))

        h1 = img_exp.histogram()
        h2 = img_cur.histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a, b: (a-b)**2, h1, h2))/len(h1))

        self.assertNotEqual(rms == 0, 'Screen valid')
