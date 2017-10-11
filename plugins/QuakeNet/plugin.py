###
# Copyright (c) 2017, Athanasius
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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('QuakeNet')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class QuakeNet(callbacks.Plugin):
    """Handle QuakeNet specific functionality, such as Q-Auth"""
    def __init__(self, irc):
        self.__parent = super(QuakeNet, self)
        self.__parent.__init__(irc)

        self.qauthed = False

    def reset(self):
        self.qauthed = False
        self.waitingJoins = {}

    def do376(self, irc, msg):
        self.log.debug("QuakeNet: do376 (end of MTOD), irc.network = '%s'" % (irc.network))
        if irc.network != "quakenet":
            return

        self.qauthed = False

        qnick = self.registryValue("qNickname")
        qaccountname = self.registryValue("qAccountNickname")
        qaccountpassword = self.registryValue("qAccountPassword")

        if qnick is None or qaccountname is None or qaccountpassword is None:
            return
        if qaccountname is not '' and qaccountpassword is not '' and qnick is not '':
            self.log.info("QuakeNet: sending Q Auth command: AUTH")
            irc.queueMsg(ircmsgs.privmsg(qnick, "AUTH " + qaccountname + " " + qaccountpassword))

    def doJoin(self, irc, msg):
        channel = msg.args[0]
        if ircutils.strEqual(irc.nick, msg.nick):
            irc.queueMsg(ircmsgs.privmsg(channel, "Cmdr Jameson reporting for duty! <o"))

    def outFilter(self, irc, msg):
        if irc.network == "quakenet" and msg.command == 'JOIN':
            if not self.qauthed:
                if self.registryValue('noJoinsUntilQAuthed'):
                    self.log.info('Holding JOIN to %s until Q Authed.',
                                  msg.args[0])
                    self.waitingJoins.setdefault(irc.network, [])
                    self.waitingJoins[irc.network].append(msg)
                    return None
        return msg

    def on396(self, irc, msg):
    # irc_396:  'port80a.se.quakenet.org' 'Cmdr.users.quakenet.org :is now your hidden host' [Cmdr.users.quakenet.org, is now your hidden host]
        self.qauthed = True
        waitingJoins = self.waitingJoins.pop(irc.network, None)
        if waitingJoins:
            for m in waitingJoins:
                irc.sendMsg(m)

Class = QuakeNet


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=0:
