# -*- coding: utf-8 -*-
from six import print_, reraise
from six import BytesIO, StringIO
from six import b, u

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
    def __init__(
        self, command, command_args, login_password, sudo_password,
        timeout = DEFAULT_TIMEOUT, expect_delay = DEFAULT_EXPECT_DELAY,
        debug_enabled = False, expect = None, expect_out = None
    ):
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.timeout = timeout
        self.expect_delay = expect_delay
        self.log = create_logger(None, debug_enabled)
        self.expect_patterns = [
            b('^Enter passphrase.+'),
            b('[Pp]assword[^\n]*:'),
            u('パスワード').encode('utf-8'), # TODO: japanese character expected as utf-8
        ]
        if expect_out is None:
            #expect_out = StringIO()
            expect_out = BytesIO()
        if expect is None:
            self.expect = pexpect.spawn(
                command,
                command_args,
                timeout = timeout,
                logfile = expect_out
            )
        else:
            self.expect = expect
        self.expect_out = expect_out
        self.log.debug("command = %s, command_args = %s" % (command, str(command_args)))

    def execute(self):
        """
        Execute a command with expect.
        
        Returns: command result status, output string
        """
        try:
            index = self.expect.expect(self.expect_patterns)
            self.log.debug("expect index = %d" % (index))
            password = self.login_password or self.sudo_password
            if index in (0, 1, 2):
                if password is None:
                    self.log.debug("Password is None")
                    #print_('[error] Password is empty. Use -l or -s', file=stderr)
                    raise CommandError("Password is empty. Use -l/--prompt-login-password or --login-password-stdin.")

                if index == 0:
                    self.expect.sendline(self.login_password) # for ssh passphrase
                else:
                    self.expect.sendline(password)
                index2 = self.expect.expect(self.expect_patterns)
                self.log.debug("expect index2 = %d" % (index2))
                if index2 == 0:
                    self.expect.sendline(self.login_password) # for ssh passphrase
                else:
                    self.expect.sendline(password)
                self.expect.expect(pexpect.EOF)
            if index == 3:
                self.log.debug("expect.EOF")
        except pexpect.TIMEOUT:
            self.log.debug("expect.TIMEOUT")
            # TODO: test
            #self.expect.close()
            raise TimeoutError("Execution is timed out after %d seconds" % (self.timeout))
        except pexpect.EOF:
            self.log.debug("expect.EOF")
        except CommandError:
            e = sys.exc_info()[1]
            #raise(e, None, sys.exc_info()[2])
            reraise(*sys.exc_info())
        return self.get_status_and_output(self.expect, self.expect_out)

    def get_status_and_output(self, child, expect_out):
        # Need a litte bit sleep because of failure of expect
        time.sleep(self.expect_delay)
        child.close()
        self.log.debug("child closed.")

        exit_status = child.exitstatus
        if exit_status is None:
            exit_status = 1
        self.log.debug("exit_status = %d" % exit_status)

        output_lines = []
        expect_regexs = [ re.compile(p.decode('utf-8')) for p in self.expect_patterns ]
        expect_regexs.append(re.compile('Connection to .* closed'))

        passwords = []
        if self.login_password:
            passwords.append(self.login_password)
        if self.sudo_password:
            passwords.append(self.sudo_password)
        #print("--- bytes ---")
        #print(expect_out.getvalue())
        lines = expect_out.getvalue().decode("utf-8").split('\n')
        #for line in expect_out.getvalue().split('\n'):
        for line in lines:
            line = line.strip('\r\n')
            if line == '' or line in passwords:
                continue

            for password in passwords:
                # for debug output
                if line == password:
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
