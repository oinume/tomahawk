# -*- coding: utf-8 -*-
import os
import sys
from tomahawk.log import create_logger

__all__ = ("Context", "Base")

class Context(object):
    """
    """
    def __init__(self, bin_dir, arguments, options, arg_parser):
        self.bin_dir = bin_dir
        self.arguments = arguments
        self.options = options
        self.arg_parser = arg_parser

class RsyncContext(Context):
    """
    """
    def __init__(self, bin_dir, source, destination, options, arg_parser):
        super(RsyncContext, self).__init__(bin_dir, None, options, arg_parser)
        self.source = source
        self.destination = destination

class BaseMain(object):
    def __init__(self, context, log=None):
        self.context = context
        if log is None:
            self.log = create_logger(context.options.debug)
        else:
            self.log = log

    def run(self):
        raise Exception("Implement by sub-class")

    def check_hosts(self):
        options = self.context.options
        if options.hosts is not None and options.hosts_files is not None:
            self.log.error('Cannot specify both options --hosts and --hosts-files.')
            self.log.error(self.context.arg_parser.format_usage())
            sys.exit(2)

        # initialize target hosts with --hosts or --hosts-files
        hosts = []
        # TODO: \, escape handling
        # regexp: [^\\],
        if options.hosts is not None:
            list = options.hosts.split(',')
            for host in list:
                host.strip()
                hosts.append(host)
        elif options.hosts_files is not None:
            list = options.hosts_files.split(',')
            for file in list:
                for line in open(file):
                    host = line.strip()
                    if host == '' or host.startswith('#'):
                        continue
                    hosts.append(host)
        else:
            self.log.error('Specify --hosts or --hosts-files option.')
            self.log.error(self.context.arg_parser.format_usage())
            sys.exit(2)

        return hosts

    def confirm_execution_on_production(self, message):
        if os.environ.get('TOMAHAWK_ENV') != 'production':
            return

        input = raw_input(message)
        if input == 'yes':
            print
        else:
            print 'Command execution was cancelled.'
            sys.exit(0)
