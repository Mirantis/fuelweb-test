from engine.poteen.bots.waitBot import WaitBot
from engine.poteen.elements.basic.button import Button
from engine.poteen.elements.basic.htmlElement import HtmlElement
from engine.poteen.log.result import Result
from tests.components.generic.abstractView import AbstractView


class Releases_BrowseView(AbstractView):
    def __init__(self, parent=None):
        self.release_name = HtmlElement(
            xpath='.//td[@class="release-name" '
                  'and contains(text(), "{name}")]',
            element_name="Release name {name}"
        )

        self.release_version = HtmlElement(
            xpath='.//tr[td[@class="release-name" '
                  'and contains(text(), "{name}")]]'
                  '/td[@class="release-version"]',
            element_name="Release {name} version"
        )

        self.release_status = HtmlElement(
            xpath='.//tr[td[@class="release-name" '
                  'and contains(text(), "{name}")]]'
                  '/td[@class="release-status"]',
            element_name="Release {name} status"
        )

        self.configure = Button(
            xpath='.//tr[td[@class="release-name" '
                  'and contains(text(), "{name}")]]'
                  '//button[contains(@class,"btn-rhel-setup")]',
            element_name="Release {name} configure button"
        )

        self.download_progress_bar = HtmlElement(
            xpath='.//tr[td[@class="release-name" '
                  'and contains(text(), "{name}")]]'
                  '//div[@class="bar-title"]',
            element_name="Release {name} download  progress bar"
        )

        AbstractView.__init__(self, parent)
        self.url = "#releases"

    def wait_for_progress_bar_disappears(self, release_name):
        res = WaitBot().wait_for_disappears(
            self.download_progress_bar._by,
            self.download_progress_bar._value.format(name=release_name),
            self._parent, 20)
        return Result("Wait for download progress bar disappears", res)
