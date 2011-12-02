# -*- coding: utf-8 -*-
import cStringIO
import pexpect
import re
import sys
import time
from tomahawk.constants import (
    DEFAULT_TIMEOUT,
    DEFAULT_EXPECT_DELAY,
    CommandError,
    TimeoutError
)
from tomahawk.log import create_logger

class CommandWithExpect(object):

    """
    A command executor through expect.
    """
    def __init__(self, command, command_args, login_password,
                 sudo_password, timeout = DEFAULT_TIMEOUT,
                 expect_delay = DEFAULT_EXPECT_DELAY, debug_enabled = False):
        self.command = command
        self.command_args = command_args
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.timeout = timeout
        self.expect_delay = expect_delay
        self.log = create_logger(debug_enabled)
        self.expect_patterns = [
            '^Enter passphrase.+',
            '[Pp]assword.*:',
            'パスワード', # TODO: japanese character expected as utf-8
        ]

    def execute(self):
        """
        Execute a command with expect.
        
        Returns: command result status, output string
        """
        expect_output = cStringIO.StringIO()
        child = pexpect.spawn(
            self.command,
            self.command_args,
            timeout = self.timeout,
            logfile = expect_output
        )
        self.log.debug("command = %s, args = %s" % (self.command, str(self.command_args)))

        try:
            index = child.expect(self.expect_patterns)
            self.log.debug("expect index = %d" % (index))

            if index in (0, 1, 2):
                password = self.sudo_password or self.login_password
                if password is None:
                    self.log.debug("Password is None")
                    #print >> stderr, "[error] Password is empty. Use -l or -s"
                    raise CommandError("Password is empty. Use -l or -s .")

                child.sendline(password)
                index2 = child.expect(self.expect_patterns)
                self.log.debug("expect index2 = %d" % (index2))
                child.sendline(password)
                child.expect(pexpect.EOF)
            if index == 3:
                self.log.debug("expect.EOF")
        except pexpect.TIMEOUT:
            self.log.debug("expect.TIMEOUT")
            raise TimeoutError("Execution is timed out after %d seconds" % (self.timeout))
        except pexpect.EOF:
            self.log.debug("expect.EOF")
        return self.get_status_and_output(child, expect_output)

    def get_status_and_output(self, child, expect_output):
        # Need a litte bit sleep because of failure of expect
        time.sleep(self.expect_delay)
        child.close()
        self.log.debug("child closed.")

        exit_status = child.exitstatus
        if exit_status is None:
            exit_status = 1
        self.log.debug("exit_status = %d" % exit_status)

        output_lines = []
        expect_regexs = [ re.compile(p) for p in self.expect_patterns ]
        passwords = []
        if self.login_password:
            passwords.append(self.login_password)
        if self.sudo_password:
            passwords.append(self.sudo_password)

        for line in expect_output.getvalue().split('\n'):
            line = line.strip('\r\n')
            if line == '' or line in passwords:
                continue
            for password in passwords:
                line = line.replace(password, len(password) * '*')

            self.log.debug("line = " + line)
            append = True
            for regex in expect_regexs:
                if regex.search(line):
                    append = False
                    continue
            if append:
                output_lines.append(line)

        output_text = '\n'.join(output_lines)
        self.log.debug("output_text = " + output_text)

        return exit_status, output_text
