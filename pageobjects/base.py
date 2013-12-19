from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
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

    @property
    def logo(self):
        return self.parent.find_element_by_css_selector('div.logo')

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
