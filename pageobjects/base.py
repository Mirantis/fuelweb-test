from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
import time
import browser


class PageObject:

    XPATH_RADIO = '//div[@class="custom-tumbler" ' \
                  'and input[@type="radio" and @name="{}" and @value="{}"]]'

    XPATH_CHECKBOX = \
        '//div[@class="custom-tumbler" ' \
        'and input[@type="checkbox" and @name="{}"]]'

    def __init__(self, parent=None):
        self.parent = parent or browser.driver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def wait_until_moving(element, timeout=10):
        class Move:
            def __init__(self, elem):
                self.element = elem
                self.location = elem.location

            def __call__(self, *args, **kwargs):
                loc = element.location
                res = self.location['x'] == loc['x'] and self.location['y'] == loc['y']
                self.location = loc
                return res

        wait = WebDriverWait(browser.driver, timeout)
        wait.until(Move(element))

    @staticmethod
    def wait_until_exists(element, timeout=10):
        wait = WebDriverWait(browser.driver, timeout)
        try:
            wait.until(lambda driver: not element.is_displayed())
        except StaleElementReferenceException as e:
            pass


class Popup(PageObject):

    def __init__(self):
        element = browser.driver.find_element_by_css_selector('div.modal')
        PageObject.__init__(self, element)
        time.sleep(0.5)
        PageObject.wait_until_moving(self.parent)

    def wait_until_exists(self):
        PageObject.wait_until_exists(
            browser.driver.find_element_by_css_selector('div.modal-backdrop'))

    @property
    def close_cross(self):
        return self.parent.find_element_by_css_selector('.close')

    @property
    def header(self):
        return self.parent.find_element_by_css_selector('.modal-header > h3')


class ConfirmPopup(Popup):

    TEXT = 'Settings were modified but not saved'

    @property
    def stay_on_page(self):
        return self.parent.find_element_by_css_selector('.btn-return')

    @property
    def leave_page(self):
        return self.parent.find_element_by_css_selector('.proceed-btn')