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
        # prompt when production environment
        self.confirm_execution_on_production(
            'Command "%s" will be executed to %d hosts. Are you sure? [yes/NO]: '
            % (' '.join(context.arguments), len(hosts))
        )

        executor = CommandExecutor(context, self.log, hosts)
        return executor.execute(context.arguments)

class RsyncMain(BaseMain):
    """
    Main class for tomahawk-rsync
    """
    def run(self):
        context = self.context
        hosts = self.check_hosts()
        # prompt when production environment
        rsync_command = 'rsync %s %s %s' % (context.options.rsync_options, context.source, context.destination)
        self.confirm_execution_on_production(
            'Rsync command "%s" will be executed %d hosts. Are you sure? [yes/NO]: '
            % (rsync_command, len(hosts))
        )

        executor = RsyncExecutor(context, self.log, hosts)
        return executor.execute(context.source, context.destination)
