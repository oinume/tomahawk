# -*- coding: utf-8 -*-
# This code is stolen from pssh-2.2.2

def create_coloring_object(stream):
    if has_colors(stream):
        return ColoringEnabled()
    else:
        return ColoringDisabled()

class ColoringDisabled(object):
    def bold(self, string): return string
    def red(self, string): return string
    def green(self, string): return string
    def yellow(self, string): return string
    def blue(self, string): return string
    def magenta(self, string): return string
    def cyan(self, string): return string
    def white(self, string): return string

class ColoringEnabled(ColoringDisabled):
    def bold(self, string): return bold(string)
    def red(self, string): return red(string)
    def green(self, string): return green(string)
    def yellow(self, string): return yellow(string)
    def blue(self, string): return blue(string)
    def magenta(self, string): return magenta(string)
    def cyan(self, string): return cyan(string)
    def white(self, string): return white(string)

def with_color(string, fg, bg=49):
    '''Given foreground/background ANSI color codes, return a string that,
    when printed, will format the supplied string using the supplied colors.
    '''
    return "\x1b[%dm\x1b[%dm%s\x1b[39m\x1b[49m" % (fg, bg, string)

def bold(string):
    '''Returns a string that, when printed, will display the supplied string
    in ANSI bold.
    '''
    return "\x1b[1m%s\x1b[22m" % string

def red(string): return with_color(string, 31) # Red
def green(string): return with_color(string, 32) # Green
def yellow(string): return with_color(string, 33) # Yellow
def blue(string): return with_color(string, 34) # Blue
def magenta(string): return with_color(string, 35) # Magenta
def cyan(string): return with_color(string, 36) # Cyan
def white(string): return with_color(string, 37) # White

#following from Python cookbook, #475186
def has_colors(stream):
    '''Returns boolean indicating whether or not the supplied stream supports
    ANSI color.
    '''
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
