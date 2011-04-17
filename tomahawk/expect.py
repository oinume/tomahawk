# -*- coding: utf-8 -*-
from cStringIO import StringIO
from pexpect import spawn, EOF, TIMEOUT
from sys import stderr
from tomahawk.constants import DEFAULT_TIMEOUT, FatalError, TimeoutError

class CommandWithExpect(object):
    """
    A command executor through expect.
    """
    def __init__(self, command, command_args, login_password, sudo_password, timeout = DEFAULT_TIMEOUT):
        self.command = command
        self.command_args = command_args
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.timeout = timeout

    def execute(self):
        """
        Execute a command with expect.
        
        Returns: command result status, output string
        """
        output = StringIO()
        #print("##### self.command = '%s', self.command_args = '%s'" % (self.command, self.command_args))
        child = spawn(
            self.command,
            self.command_args,
            timeout = self.timeout,
            logfile = output, # TODO: logfile -> child.before() or child.after()
        )
        #child.logfile_send = file('/tmp/expect_send', 'w')
        #child.logfile = sys.stdout
        # print "%s %s" % (self.command, str(self.command_args))

        login_expect = r"^(.+'s password:?\s*|Enter passphrase.+)"
        sudo_expect0 = r'^[Pp]assword:?\s*$'
        sudo_expect1 = '^([Pp]assword:?\s*|パスワード:\s*)' # TODO: japanese character expected as utf-8
        sudo_expect2 = '^\[sudo\] password for.+$'
        try:
            #print("##### before child.expect()")
            index = child.expect([ login_expect, sudo_expect0, sudo_expect1, sudo_expect2 ])
            if index == 0: # login_expect
                if self.login_password is None:
                    # SSH authentication required but login_password is not input,
                    # so notify --prompt-login-password option
                    print >> stderr, '[warn] Use --prompt-login-password for ssh authentication.'
                    child.sendline()
                    child.expect(EOF)
                    child.kill(0)
                else:
                    child.sendline(self.login_password)
                    child.expect(EOF)
            elif index in (1, 2, 3): # might be sudo_expect
                #print "sudo expect. index = " + str(index)
                # Because some OSes (like MacOS) prompt 'Password:' for SSH authentication,
                # send login_password if sudo_password isn't provided
                child.sendline(self.sudo_password or self.login_password)
                child.expect(EOF)
            else:
                raise FatalError("Should not reach here")

        except EOF:
            #print "##### except EOF"
            pass
        except TIMEOUT:
            #print "##### except TIMEOUT"
            raise TimeoutError("Execution is timed out after %d seconds" % (self.timeout))

        child.close()
        exit_status = child.exitstatus
        #print "exit_status = %d" % exit_status

        output_tmp = output.getvalue()
        output_text = ''
        password = self.login_password or self.sudo_password
        if password is not None:
            for line in output_tmp.splitlines():
                if line.endswith(password):
                    continue
                output_text += line + '\n'
        else:
            output_text = output_tmp

#        print "output = '%s'" % output_text
        output.close()

        return exit_status, output_text.strip()
