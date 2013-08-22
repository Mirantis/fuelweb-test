from selenium.webdriver.common.by import By
from engine.poteen.basePage import BasePage
from engine.poteen.bots.actionBot import ActionBot
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.elements.basic.radio import Radio as EngineRadio
from engine.poteen.error import TestExecutionRuntimeException


class Table(BasePage):
    def __init__(self, table):
        self.rows = [
            HtmlElement(element=element)
            for element in self.get_action_bot().find_elements(
                by=By.XPATH, value="./tbody/tr", parent=table
            )
        ]
        self.cell = HtmlElement(
            xpath="./tbody/tr[{row}]/td[{column}]",
            element_name="cell"
        )
        BasePage.__init__(self, parent=table)

    def get_rows_count(self):
        return len(self.rows)

    def get_value(self, row, column):
        return self.cell.find(
            row=row,
            column=column
        ).get_value()

    def get_row(self, column, name):
        for i in range(1, self.get_rows_count() + 1):
            if self.get_value(i, column) == name:
                return i
        raise TestExecutionRuntimeException(
            "Row not found with column [{id}] equals to [{name}]".format(
                name=name, id=column
            )
        )

    def verify_value(self, row, column, value):
        return self.get_verify_bot().verify_contains(
            value,
            self.get_value(row, column),
            "row: {row}, column: {column}".format(row=row, column=column),
            "table cell"
        )
