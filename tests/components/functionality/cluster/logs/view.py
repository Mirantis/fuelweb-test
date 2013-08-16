from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.select import Select
from engine.poteen.log.resultList import ResultList

from ....generic.abstractView import AbstractView


class Cluster_Logs_View(AbstractView):

    def __init__(self, parent=None):
        self.log_node = Select(
            xpath=".//div[contains(@class,'log-type-filter')]/select",
            element_name="Logs")

        self.source = Select(
            xpath=".//div[contains(@class,'log-source-filter')]/select",
            element_name="Source")

        self.level = Select(
            xpath=".//div[contains(@class,'log-level-filter')]/select",
            element_name="Min. level")

        self.show_button = Button(
            xpath=".//button[contains(@class,'show-logs-btn')]",
            element_name="Show")

        self.table_logs = HtmlElement(
            xpath=".//table[contains(@class,'table-logs')]",
            element_name="Logs table")

        AbstractView.__init__(self, parent)

    def set_log(self, value):
        return self.log_node.set_value(value)

    def set_source(self, name, value):
        return self.source.set_value(value)

    def set_level(self, name, value):
        return self.level.set_value(value)

    def set_log_filter(self, log, source, level):
        return ResultList("Set log filter parameters")\
            .push(self.log_node.set_value(log))\
            .push(self.source.set_value(source))\
            .push(self.level.set_value(level))