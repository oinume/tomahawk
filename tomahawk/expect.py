# -*- coding: utf-8 -*-
from cStringIO import StringIO
from pexpect import spawn, EOF, TIMEOUT
from sys import stderr
from tomahawk.constants import DEFAULT_EXPECT_TIMEOUT

class CommandWithExpect(object):
    def __init__(self, command, login_password, sudo_password, timeout = DEFAULT_EXPECT_TIMEOUT):
        self.command = command
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.timeout = timeout

    def execute(self):
        output = StringIO()
        child = spawn(
            self.command,
            timeout = self.timeout,
            logfile = output
        )
        #child.logfile_send = file('/tmp/expect_send', 'w')
        #child.logfile = sys.stdout

        #print "command = " + self.command
        login_expect = "^(.+'s password:?\s*|Enter passphrase.+)"
        sudo_expect1 = '^([Pp]assword:?\s*|パスワード:\s*)' # TODO: japanese character expected as utf-8
        sudo_expect2 = '^\[sudo\] password for.+$'
        try:
            index = child.expect([ login_expect, sudo_expect1, sudo_expect2 ])
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
            elif index in (1, 2): # might be sudo_expect
                #print "sudo expect. index = " + str(index)
                # Because some OSes (like MacOS) prompt 'Password:' for SSH authentication,
                # send login_password if sudo_password isn't provided
                child.sendline(self.sudo_password or self.login_password)
                child.expect(EOF)
            else:
                raise RuntimeError('Should not reach here')

        except EOF:
            pass
            #print "EOF"
        except TIMEOUT:
            pass
            #print "timeout"
        
        child.close()
        exit_status = child.exitstatus
        #print "exit_status = %d" % exit_status

        output_text = output.getvalue()
        #print "output = '%s'" % output_text
        output.close()

        return exit_status, output_text.strip()

"""
sub print_for_expect {
    my ($self, @args) = @_;
    unless ($self->{print_for_expect_enabled}) {
        return;
    }
    $self->{captures} ||= [];
    
    my $line = join("", @args);
    chomp $line;
    push @{ $self->{captures} }, $line;
}

sub print_for_expect_flush {
    my ($self) = @_;
    $self->{captures} = [];
}

sub execute_by_expect {
    my ($self, $command) = @_;
    my $login_password = $self->login_password;
    my $sudo_password = $self->sudo_password;

    my $expect = Expect->new($command) or return -1;
    $expect->log_stdout(0);
    $expect->log_file(sub { $self->print_for_expect(@_) });

    my $expect_timeout = $self->context->options->{'expect-timeout'} || 10;
    my $login_expect_regexp = qr/^(.+'s password:\s*|Enter passphrase.+)/;
    my $sudo_expect_regexp = qr/^([Pp]assword:\s*|パスワード:\s*)$/;
    $expect->expect(
        $expect_timeout,
        [
            $login_expect_regexp => sub {
                unless (defined $login_password) {
                    # SSHのログイン認証が走っているが、$login_passwordが入力されていないので
                    # --prompt-login-password オプションの存在を知らせておく
                    warn "[warn] Use --prompt-login-password for ssh authentication.\n";
                    $expect->send("\n");
                    return exp_continue;
                }
                $self->{print_for_expect_enabled} = 0;
                $expect->send($login_password . "\n");
                exp_continue;
            },
        ],
        [
            $sudo_expect_regexp => sub {
                $self->{print_for_expect_enabled} = 0;
                $expect->send($sudo_password . "\n");
                exp_continue;
            }
        ],
        [
            qr/.+/ => sub {
                $self->{print_for_expect_enabled} = 1;
                exp_continue;
            }
        ],
        [
            timeout => sub {
                croak "Expect timeout.\n"
            }
        ],
    );

    for my $line (@{ $self->{captures} }) {
        if ($line =~ $login_expect_regexp || $line =~ $sudo_expect_regexp) {
            next;
        }
        verbose($line);
    }
    $self->print_for_expect_flush;
    $expect->hard_close;

    return $expect->exitstatus;
}
"""
