#!/usr/bin/env python

__author__ = "Mark Nottingham <mnot@mnot.net>"
__copyright__ = """\
Copyright (c) 2008-2012 Mark Nottingham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import re
from urlparse import urljoin

import redbot.speak as rs
import redbot.headers as rh
import redbot.http_syntax as syntax


# The most common problem with Location is a non-absolute URI, 
# so we separate that from the syntax check.
@rh.CheckFieldSyntax(syntax.URI_reference, rh.rfc2616 % "sec-14.30")
def parse(subject, value, red):
    if red.res_status not in [
        "201", "300", "301", "302", "303", "305", "307"
    ]:
        red.set_message(subject, rs.LOCATION_UNDEFINED)
    if not re.match(r"^\s*%s\s*$" % syntax.URI, value, re.VERBOSE):
        red.set_message(subject, rs.LOCATION_NOT_ABSOLUTE,
                        full_uri=urljoin(red.uri, value))
    return value

@rh.SingleFieldValue
def join(subject, values, red):
    return values[-1]