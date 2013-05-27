from engine.poteen.elements.basic.button import Button
from ....generic.abstractView import AbstractView


class Cluster_Actions_View(AbstractView):
    delete = Button(
        xpath="//div[@id='content']"
              "//button[contains(@class, 'delete-cluster-btn')]",
        element_name="Delete")

    def __init__(self, parent=None):
        AbstractView.__init__(self, parent)

    def click_delete_cluster_button(self):
        return self.delete.click()