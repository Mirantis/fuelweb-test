import os
import sys

import nose

from engine.poteen.utils.plugin.poteenRunnerPlugin import PoteenRunnerPlugin


if __name__ == '__main__':
    nose.main(
        argv=[os.path.dirname(os.path.abspath(__file__))] + sys.argv[1:]
             + ["--with-poteenrunnerplugin"],
        addplugins=[PoteenRunnerPlugin()]
    )
