#!/usr/bin/env python

###
# Copyright (c) 2002, Jeremiah Fincher
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

from test import *

import Alias


class FunctionsTest(unittest.TestCase):
    def testFindAliasCommand(self):
        s = 'command'
        self.failIf(Alias.findAliasCommand(s, ''))
        self.failIf(Alias.findAliasCommand(s, 'foo'))
        self.failIf(Alias.findAliasCommand(s, 'foo bar [  baz]'))
        self.failIf(Alias.findAliasCommand(s, 'foo bar [baz]'))
        self.failUnless(Alias.findAliasCommand(s, s))
        self.failUnless(Alias.findAliasCommand(s, '  %s' % s))
        self.failUnless(Alias.findAliasCommand(s, '[%s]' % s))
        self.failUnless(Alias.findAliasCommand(s, '[ %s]' % s))
        self.failUnless(Alias.findAliasCommand(s, 'foo bar [%s]' % s))
        self.failUnless(Alias.findAliasCommand(s, 'foo bar [ %s]' % s))

    def testFindBiggestDollar(self):
        self.assertEqual(Alias.findBiggestDollar(''), None)
        self.assertEqual(Alias.findBiggestDollar('foo'), None)
        self.assertEqual(Alias.findBiggestDollar('$0'), 0)
        self.assertEqual(Alias.findBiggestDollar('$1'), 1)
        self.assertEqual(Alias.findBiggestDollar('$2'), 2)
        self.assertEqual(Alias.findBiggestDollar('$3'), 3)
        self.assertEqual(Alias.findBiggestDollar('foo bar $1'), 1)
        self.assertEqual(Alias.findBiggestDollar('foo $2 $1'), 2)
        self.assertEqual(Alias.findBiggestDollar('foo $0 $1'), 1)
        self.assertEqual(Alias.findBiggestDollar('foo $1 $3'), 3)
        self.assertEqual(Alias.findBiggestDollar('$10 bar $1'), 10)
