from selenium.webdriver.support.select import Select
from pageobjects.base import PageObject


class Nodes(PageObject):

    @property
    def info_icon(self):
        return self.parent.find_element_by_css_selector('i.icon-info-circled')

    @property
    def env_name(self):
        return self.parent.find_element_by_css_selector('span.btn-cluster-details')

    @property
    def env_details(self):
        return self.parent.find_element_by_css_selector('ul.cluster-details')

    @property
    def group_by(self):
        return Select(self.parent.find_element_by_css_selector('select[name=grouping]'))
