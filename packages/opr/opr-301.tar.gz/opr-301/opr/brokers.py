# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0212,W0718,E0402,W0201,W0613,E1120,R0902


"broker"


class Broker:

    objs = []

    @staticmethod
    def add(obj) -> None:
        Broker.objs.append(obj)

    @staticmethod
    def remove(obj) -> None:
        try:
            Broker.objs.remove(obj)
        except ValueError:
            pass


def announce(txt):
    for obj in Broker.objs:
        obj.announce(txt)

def byorig(orig):
    for obj in Broker.objs:
        if object.__repr__(obj) == orig:
            return obj
    return None


def bytype(typ):
    for obj in Broker.objs:
        if typ in object.__repr__(obj):
            return obj
    return None


def say(orig, channel, txt):
    bot = byorig(orig)
    if not bot:
        return
    bot.dosay(channel, txt)
