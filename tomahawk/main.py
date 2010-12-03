# -*- coding: utf-8 -*-
from tomahawk.command_line import BaseMain
from tomahawk.executors import CommandExecutor, RsyncExecutor

class Main(BaseMain):
    """
    Main class for tomahawk
    """
    def run(self):
        context = self.context
        hosts = self.check_hosts()

        # TODO: prompt when production (defined in tomahawk.conf or ENV)
        executor = CommandExecutor(context, self.log, hosts)
        return executor.execute(context.arguments)


class RsyncMain(BaseMain):
    """
    Main class for tomahawk-rsync
    """
    def run(self):
        context = self.context
        hosts = self.check_hosts()

        # TODO: prompt when production (defined in tomahawk.conf or ENV)
        executor = RsyncExecutor(context, self.log, hosts)
        return executor.execute(context.source, context.destination)
