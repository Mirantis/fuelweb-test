from optparse import OptionGroup
from nose.plugins import Plugin
from ..settings import RED_HAT


class CredentialsParserPlugin(Plugin):

    def __init__(self):
        super(CredentialsParserPlugin, self).__init__()

    def options(self, parser, env):
        super(CredentialsParserPlugin, self).options(parser, env)
        group = OptionGroup(parser, "Options of RedHat credentials parser")

        group.add_option(
            '--rh-username',
            dest='rh_username',
            action='store',
            help='Set red hat username')
        group.add_option(
            '--rh-password',
            dest='rh_password',
            action='store',
            help='set red hat password')
        group.add_option(
            '--rh-server',
            dest='rh_server',
            action='store',
            help='Set satellite server hostname')
        group.add_option(
            '--rh-activation-key',
            dest='rh_activation_key',
            action='store',
            help='Set activation key')

        parser.add_option_group(group)

    def configure(self, options, conf):
        super(CredentialsParserPlugin, self).configure(options, conf)
        if hasattr(options, "rh_username"):
            RED_HAT["username"] = getattr(options, "rh_username")
        if hasattr(options, "rh_password"):
            RED_HAT["password"] = getattr(options, "rh_password")
        if hasattr(options, "rh_server"):
            RED_HAT["satellite server hostname"] = \
                getattr(options, "rh_server")
        if hasattr(options, "rh_activation_key"):
            RED_HAT["activation key"] = getattr(options, "rh_activation_key")
