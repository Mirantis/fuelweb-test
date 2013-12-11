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