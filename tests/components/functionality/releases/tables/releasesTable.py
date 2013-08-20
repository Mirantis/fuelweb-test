from sqlalchemy.sql.expression import column
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement

from .....components.elements.Table import Table
from engine.poteen.log.result import Result
from engine.poteen.log.resultList import ResultList


class Releases_Table(Table):

    def __init__(self):
        self.configure = Button(
            xpath="./tbody/tr[{row}]/td[{column}]/button",
            element_name="Configure"
        )
        self.progress = HtmlElement(
            xpath="./tbody/tr[{row}]/td[{column}]"
                  "//div[contains(@class, 'progress')]",
            element_name="progress bar"
        )
        Table.__init__(self, HtmlElement(
            xpath=".//table[contains(@class, 'releases-table')]",
            element_name="Releases table"
        ).get_element())

    def get_release_row(self, release_name):
        return self.get_row(1, release_name)

    def get_release_status(self, release_name):
        return self.get_value(self.get_release_row(release_name), 3)

    def click_configure(self, release_name):
        return self.configure.find(
            row=self.get_row(1, release_name),
            column=4
        ).click()

    def verify_releases_count(self, count):
        return self.get_verify_bot().verify_equal(
            count, self.get_rows_count(), "Releases table", "rows count"
        )

    def verify_release_status(self, release_name, status):
        return self.get_verify_bot().verify_equal(
            expected=status,
            actual=self.get_release_status(release_name),
            name=release_name,
            _type="status"
        )

    def wait_downloading(self, release_name):
        rl = ResultList(
            "Wait release downloading done: {}".format(release_name))
        row = self.get_release_row(release_name=release_name)
        rl.push(self.progress.find(row=row, column=3).verify_visible(True))
        rl.info("Release download started")
        if self.get_wait_bot().wait_for_web_element_disappears(
                web_element=self.progress.get_element(),
                timeout=20,
                poll_frequency=3) is not None:
            rl.info("Release download done")
        else:
            rl.push(Result("Release download failed on timeout", False))
        return rl
