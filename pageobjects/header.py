from pageobjects.base import PageObject


class Header(PageObject):

    @property
    def logo(self):
        return self.parent.find_element_by_css_selector('div.logo')

    @property
    def environments(self):
        return self.parent.find_element_by_css_selector('.navigation-bar-ul a[href$=clusters]')

    @property
    def releases(self):
        return self.parent.find_element_by_css_selector('.navigation-bar-ul a[href$=releases]')

    @property
    def support(self):
        return self.parent.find_element_by_css_selector('.navigation-bar-ul a[href$=support]')

    @property
    def breadcrumb(self):
        return self.parent.find_element_by_css_selector('.breadcrumb')

    @property
    def total_nodes(self):
        return self.parent.find_element_by_css_selector('div.total-nodes-count')

    @property
    def unallocated_nodes(self):
        return self.parent.find_element_by_css_selector('div.unallocated-nodes-count')