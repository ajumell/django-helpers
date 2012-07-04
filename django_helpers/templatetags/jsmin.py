# This code is original from jsmin by Douglas Crockford, it was translated to
# Python by Baruch Even. It was refactored by Dave St.Germain for speed.
# The original code had the following copyright and license.
#
# /* jsmin.c
#    2007-01-08
#
# Copyright (c) 2002 Douglas Crockford  (www.crockford.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# The Software shall be used for Good, not Evil.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# */

import sys
from django import template

is_3 = sys.version_info >= (3, 0)
if is_3:
    import io
else:
    import StringIO

    try:
        import cStringIO
    except ImportError:
        cStringIO = None

__all__ = ['jsmin', 'JavascriptMinify']
__version__ = '2.0.2'


def jsmin(js):
    """
    returns a minified version of the javascript string
    """
    if not is_3:
        if cStringIO and not isinstance(js, unicode):
            # strings can use cStringIO for a 3x performance
            # improvement, but unicode (in python2) cannot
            klass = cStringIO.StringIO
        else:
            klass = StringIO.StringIO
    else:
        klass = io.StringIO
    ins = klass(js)
    outs = klass()
    JavascriptMinify(ins, outs).minify()
    return outs.getvalue()


class JavascriptMinify(object):
    """
    Minify an input stream of javascript, writing
    to an output stream
    """

    def __init__(self, instream=None, outstream=None):
        self.ins = instream
        self.outs = outstream

    def minify(self, instream=None, outstream=None):
        if instream and outstream:
            self.ins, self.outs = instream, outstream
        write = self.outs.write
        read = self.ins.read

        space_strings = "abcdefghijklmnopqrstuvwxyz"\
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$\\"
        starters, enders = '{[(+-', '}])+-"\''
        newlinestart_strings = starters + space_strings
        newlineend_strings = enders + space_strings
        do_newline = False
        do_space = False
        doing_single_comment = False
        previous_before_comment = ''
        doing_multi_comment = False
        in_re = False
        in_quote = ''
        quote_buf = []

        previous = read(1)
        next1 = read(1)
        if previous == '/':
            if next1 == '/':
                doing_single_comment = True
            elif next1 == '*':
                doing_multi_comment = True
            else:
                write(previous)
        elif not previous:
            return
        elif previous >= '!':
            if previous in "'\"":
                in_quote = previous
            write(previous)
            previous_non_space = previous
        else:
            previous_non_space = ' '
        if not next1:
            return

        while 1:
            next2 = read(1)
            if not next2:
                last = next1.strip()
                if not (doing_single_comment or doing_multi_comment)\
                and last not in ('', '/'):
                    write(last)
                break
            if doing_multi_comment:
                if next1 == '*' and next2 == '/':
                    doing_multi_comment = False
                    next2 = read(1)
            elif doing_single_comment:
                if next1 in '\r\n':
                    doing_single_comment = False
                    while next2 in '\r\n':
                        next2 = read(1)
                    if previous_before_comment in ')}]':
                        do_newline = True
            elif in_quote:
                quote_buf.append(next1)

                if next1 == in_quote:
                    numslashes = 0
                    for c in reversed(quote_buf[:-1]):
                        if c != '\\':
                            break
                        else:
                            numslashes += 1
                    if numslashes % 2 == 0:
                        in_quote = ''
                        write(''.join(quote_buf))
            elif next1 in '\r\n':
                if previous_non_space in newlineend_strings\
                or previous_non_space > '~':
                    while 1:
                        if next2 < '!':
                            next2 = read(1)
                            if not next2:
                                break
                        else:
                            if next2 in newlinestart_strings\
                               or next2 > '~' or next2 == '/':
                                do_newline = True
                            break
            elif next1 < '!' and not in_re:
                if (previous_non_space in space_strings\
                    or previous_non_space > '~')\
                and (next2 in space_strings or next2 > '~'):
                    do_space = True
            elif next1 == '/':
                if (previous in ';\n\r{}' or previous < '!') and next2 in '/*':
                    if next2 == '/':
                        doing_single_comment = True
                        previous_before_comment = previous_non_space
                    elif next2 == '*':
                        doing_multi_comment = True
                else:
                    if not in_re:
                        in_re = previous_non_space in '(,=:[?!&|'
                    elif previous_non_space != '\\':
                        in_re = not in_re
                    write('/')
            else:
                if do_space:
                    do_space = False
                    write(' ')
                if do_newline:
                    write('\n')
                    do_newline = False
                write(next1)
                if not in_re and next1 in "'\"":
                    in_quote = next1
                    quote_buf = []
            previous = next1
            next1 = next2

            if previous >= '!':
                previous_non_space = previous


class JsMinNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return jsmin(output)


class JsRmLnNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        lines = output.split('\n')
        result = []
        for line in lines:
            if str(line).strip() != "":
                result.append(line)
        return "\n".join(result)


class RemoveLastComaNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        output = output.strip()
        if output[-1:] == ',':
            output = output[:-1]
        return output


def do_jsmin(parser, token):
    nodelist = parser.parse(('endjsmin',))
    parser.delete_first_token()
    return JsMinNode(nodelist)


def do_jsrmln(parser, token):
    nodelist = parser.parse(('endjsrmln',))
    parser.delete_first_token()
    return JsRmLnNode(nodelist)


def do_remove_last_coma(parser, token):
    nodelist = parser.parse(('endremovecoma',))
    parser.delete_first_token()
    return RemoveLastComaNode(nodelist)


register = template.Library()
register.tag('jsmin', do_jsmin)
register.tag('jsrmln', do_jsrmln)
register.tag('removecoma', do_remove_last_coma)
