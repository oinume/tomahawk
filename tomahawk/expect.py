# -*- coding: utf-8 -*-
from pexpect import spawn, EOF, TIMEOUT
from tomahawk.constants import DEFAULT_TIMEOUT, FatalError, TimeoutError
from tomahawk.log import create_logger

class CommandWithExpect(object):
    """
    A command executor through expect.
    """
    def __init__(self, command, command_args, login_password,
                 sudo_password, timeout = DEFAULT_TIMEOUT, debug_enabled = False):
        self.command = command
        self.command_args = command_args
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.timeout = timeout
        self.log = create_logger(debug_enabled)

    def execute(self):
        """
        Execute a command with expect.
        
        Returns: command result status, output string
        """
        child = spawn(
            self.command,
            self.command_args,
            timeout = self.timeout,
        )
        self.log.debug("command = %s, args = %s" % (self.command, str(self.command_args)))

        login_expect = '^(.+\'s password:?\s*|Enter passphrase.+)'
        sudo_expect0 = '[Pp]assword:'
        sudo_expect1 = '^パスワード:' # TODO: japanese character expected as utf-8

        try:
            index = child.expect([ login_expect, sudo_expect0, sudo_expect1, EOF ])
            self.log.debug("expect index = %d" % (index))

            if index in (0, 1, 2):
                password = self.sudo_password or self.login_password
                if password is None:
                    self.log.debug("Password is None")
                    #print >> stderr, "[error] Password is empty. Use -l or -s"
                    raise FatalError("Password is empty. Use -l or -s .")

                child.sendline(password)
            if index == 3:
                self.log.debug("expect.EOF")
        except TIMEOUT:
            self.log.debug("timeout")
            raise TimeoutError("Execution is timed out after %d seconds" % (self.timeout))
        except EOF:
            self.log.debug("EOF")
        finally:
            #child.close()
            pass
        return self.get_status_and_output(child)

    def get_status_and_output(self, child):
        lines = child.readlines()
        child.close()
        self.log.debug("child closed.")

        exit_status = child.exitstatus
        if exit_status is None:
            exit_status = 1
        self.log.debug("exit_status = %d" % exit_status)

        output_text = ''
        for line in lines:
            if line.strip() == '':
                # Ignore empty line
                continue
            output_text += line
        self.log.debug("output_text = '%s'" % output_text)

        return exit_status, output_text.strip()
