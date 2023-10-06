# coding=utf8
"""sopel-flipper

A Sopel plugin that flips text in response to CTCP ACTIONs.
"""
from __future__ import unicode_literals, absolute_import, division, print_function

from upsidedown import transform

from sopel import plugin


@plugin.rule('^flips (.+)')
@plugin.ctcp
def flips(bot, trigger):
    target = trigger.group(1).strip()
    if target in ['a table', 'the table']:
        bot.say("(╯°□°）╯︵ ┻━┻")
    else:
        bot.say("(╯°□°）╯︵ %s" % transform(target))

@plugin.rule('^rolls (.+)')
@plugin.ctcp
def roll(bot, trigger):
    target = trigger.group(1).strip()
    if target.endswith(' down a hill'):
        target = target[:-12]
        tegrat = transform(target)
        bot.say("(╮°-°)╯︵ %s %s %s %s %s (@_@;)" % (tegrat, target, tegrat, target, tegrat))
    else:
        bot.say("(╮°-°)╯︵ %s" % transform(target))
