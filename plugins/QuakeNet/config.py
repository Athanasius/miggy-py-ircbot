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

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('QuakeNet')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('QuakeNet', True)


QuakeNet = conf.registerPlugin('QuakeNet')

conf.registerGlobalValue(QuakeNet, 'qNickname',
    registry.String('Q@CServe.quakenet.org', _("""Q's fully qualified name, for privmsg""")))

conf.registerGlobalValue(QuakeNet, 'qAccountNickname',
    registry.String('', _("""Bot's Q Account Nickname""")))

conf.registerGlobalValue(QuakeNet, 'qAccountPassword',
    registry.String('', _("""Bot's Q Account Password"""), private=True))

conf.registerGlobalValue(QuakeNet, 'noJoinsUntilQauthed',
    registry.Boolean(False, _("""Determines whether the bot will not join any
    channels until it is Q Authed.  This may be useful, for instances, if
    you have a vhost that isn't set until you're Q Authed, or if you're
    joining +r channels that won't allow you to join unless you Q Authed.""")))

conf.registerGlobalValue(QuakeNet, 'channelGreeting',
    registry.String('', _("""Bot's message to send to a channel when it has just joined.""")))
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
