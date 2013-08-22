import os
import sys

import nose
from engine.poteen.contextHolder import ContextHolder
import logging
from tests.components.helpers.RHCredentialsParserPlugin \
    import CredentialsParserPlugin

ContextHolder.LOG_LEVEL = logging.DEBUG

selenium_logger = logging.getLogger(
    'selenium.webdriver.remote.remote_connection'
)
selenium_logger.setLevel(logging.WARNING)

from engine.poteen.utils.plugin.poteenRunnerPlugin import PoteenRunnerPlugin
if __name__ == '__main__':
    nose.main(
        argv=[os.path.dirname(os.path.abspath(__file__))] + sys.argv[1:] +
        ["--with-poteenrunnerplugin"]+["--with-credentialsparserplugin"],
        addplugins=[PoteenRunnerPlugin(), CredentialsParserPlugin()]
    )
