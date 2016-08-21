Changes
=======

0.7.4.1 <2016-08-21>
------------------
* bug: #57 UnicodeEncodeError (Thanks @sekino for reporting)

0.7.3 <2016-04-24>
------------------
* #54 Add Python 3.5 support
* #55 Fix line break problem when expect (Thanks @sekino)

0.7.2 <2014-07-27>
------------------
* bug: #50 pexpect-3.3 installation problem (ValueError: I/O operation on closed file)
* #49 Add Python 3.4 support

0.7.1 <2014-04-17>
------------------
* bug: #46 Cannot install latest `six' on Python 2.4 (Thanks @n0ts)
* #47 Test various environments with Vagrant
* #48 Wrong command line options in documentation

0.7.0 <2014-03-02>
------------------
* bug: #41 Ignores User configuration on $HOME/.ssh/config

0.7.0-rc1 <2013-11-16>
----------------------
* feature: #42 Python3 support
* change: #43 An alias of --hosts should be -H (not -h)
* change: #44 Delete duplicated options --expect-timeout, --no-sudo-password

0.6.0 <2013-04-21>
------------------
* document: Add "For developers" section in README.rst

0.6.0-rc1 <2013-04-06>
----------------------
* feature: #36 --verify-output option
* feature: #37 A short-cut '-F' for --output-format option
* feature: #39 -C/--conf: Specify a configuration file
* document: #38 tomahawk recipes in documentation

0.5.2 <2012-06-01>
------------------
* bug: #35 A duplicated command output.

0.5.1 <2012-05-26>
------------------
* bug: #33 tomahawk should escape '$' and '`'
* bug: #34 parallel numer should be smaller than specified value when count of hosts is smal
* document: updateUpdated documentation.
* test: Updated testing codes (now uses pytest and flexmock)

0.5.0 <2012-04-01>
------------------
* Nothing changed from 0.5.0-rc3

0.5.0-rc3 <2012-03-24>
----------------------
* More bug fixes
* change: Removed option in 0.5.0-rc1 '--prompt-login-password' were back.
* feature: #16 New options --login-password-stdin, --sudo-password-stdin is now available
* change: #32 tomahawk now doesn't prompt sudo password even if 'sudo ...' command given. If -s/--prompt-sudo-password is given, tomahawk prompts sudo password.

0.5.0-rc2 <2012-03-13>
----------------------
* bug : tomahawk doesn't stop completely when SIGINT(Ctrl-C) received

0.5.0-rc1< 2012-03-04>
----------------------
* feature: #22 Output OS version, Python version, libraries versions
* bug: #27 Should call Pool#join() after all processes are finished
* bug: #26 tomahawk-rsync should say an easier error message when rsync command is not found.
* change: #16 Now tomahawk sends command with 'ssh -t', allocates pseudo-tty.
  **This changes default behavior of `tomahawk`.**
  Sended commands on remote host will be cancelled after `tomahawk` stops. (Ctrl-C or something)
  Old behavior is that remote commands never stop even if `tomahawk` stops.
  If you want old behavior, use --ssh-options='-T'. It disables pseudo-tty allocation.

0.4.5 <2012-01-15>
------------------
* bug: Fixed installation error for 0.4.4

0.4.4 <2012-01-14>
------------------
* document: New documentation with sphinx.
* bin/tomahawk_bootstrap.py was moved to tomahawk directory. (Thanks `@mkouhei <https://github.com/mkouhei>`)
* Created tools directory for developers.

0.4.3 <2011-12-03>
------------------
* bug: #21 Support sudo prompt in Ubuntu. (Thanks t9md)
* Added files. AUTHORS, COPYING

0.4.2 <2011-11-27>
------------------
* Updated a license(LGPL -> LGPL 2.1)
* Added man page (Thanks @mkouhei)

0.4.1 <2011-09-18>
------------------
* bug: #15 setup.py is not ready for python 2.4

0.4.0 <2011-07-14>
------------------
* feature: #13 Coloring output
* feature: #14 Support python 2.4
* bug: #12 Unknown distribution option: 'test_require'
* Refactoring whole source and adding more tests

0.3.4 <2011-07-05>
------------------
* feature: #8 --output-format option for tomahawk

0.3.3 <2011-07-04>
------------------
* bug: #6 Timeout problem when both ssh authentication and sudo password required
* bug: #10 tomahawk times out when japanese sudo password prompt
* change: #11 --expect-encoding is now obsoleted
* change: #9 release.py problem

0.3.2 <2011-06-18>
------------------
* bug: #6 Timeout problem when both ssh authentication and sudo password required
* bug: #7 Password is not masked even --debug

0.3.1 <2011-06-16>
------------------
* bug: #4 Pass a directory to -f option, traceback occurrs
* bug: #6 Timeout problem when both ssh authentication and sudo password required

0.3.0 <2011-05-15>
------------------
* Improve handling keyboard interrupt.
* Fix tests.

0.3.0-rc1 <2011-04-17>
----------------------
* bug: When execution timed out, looks like just failure.
* bug: All host names are not displayed when tomahawk-rsync with --continue-on-error fails.
* bug fix: Displays error hosts with specified order when --continue-on-error option specified.
* change: --expect-timeout becomes duplicated. Use --timeout instead.
* change: Default --timeout seconds is changed from 5 to 10.
* change: Changed filename format from '%(filename)__%(host)' to '%(host)__%(filename)' when tomahawk-rsync --mirror-mode=pull.
* Output further debug messages when --debug.

0.2.6 <2011-04-13>
------------------
* feature: --no-sudo-password is now available.

0.2.5 <2011-02-24>
------------------
* bug: When no sudo password, no command output.

0.2.4 <2011-02-08>
------------------
* bug: #3 tomahawk-rsync in tomahawk-0.2.3 is broken. See https://github.com/oinume/tomahawk/issues#issue/3

0.2.3 <2011-02-07>
------------------
* bug: #2 Shell quote problem. See https://github.com/oinume/tomahawk/issues/closed#issue/2

0.2.2 <2011-01-25>
------------------
* bug: when tomahawk-rsync -m pull specified, always appends hostname to local filename.

0.2.1 <2011-01-24>
------------------
* bug: tomahawk-rsync always outputs same hostname.

0.2.0 <2010-12-07>
-------------------------------
* feature: When environment "TOMAHAWK_ENV" is "production", tomahawk confirms command execution.
* feature: --version option is now available.

0.1.2 <2010-12-06>
------------------
* bug: tomahawk prints a password to stdout.

0.1.1 <2010-12-02>
------------------
* change: Renamed. tomahawk.py -> tomahawk, tomahawk-rsync.py -> tomahawk-rsync
* Fixed many bugs

0.1.0 <2010-11-26>
--------------------------------
* The first release of python version.
* feature: Brand new option: -p (--parallel)
* change: -C option is now obsoleted. Use -c
