# Copyright (c) 2012-2013 Paul Tagliamonte <paultag@debian.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


def init():
    from debile.master.orm import init_db
    return init_db()


def process_incoming():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Debile master incoming handling")
    parser.add_argument("--no-dud", action="store_false", dest="dud",
                        help="Do not process *.dud files.")
    parser.add_argument("--no-changes", action="store_false", dest="changes",
                        help="Do not process *.changes files.")
    parser.add_argument("directory", action="store",
                        help="Directry to process.")

    from debile.master.incoming import main
    main(parser.parse_args())


def import_db():
    from debile.master.dimport import import_from_yaml
    import sys
    return import_from_yaml(*sys.argv[1:])


def server():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Debile master daemon")
    parser.add_argument("-s", "--syslog", action="store_true", dest="syslog",
                        help="Log to syslog instead of stderr.")
    parser.add_argument("-d", "--debug", action="store_true", dest="debug",
                        help="Enable debug messages to stderr.")

    from debile.master.server import main
    main(parser.parse_args())
