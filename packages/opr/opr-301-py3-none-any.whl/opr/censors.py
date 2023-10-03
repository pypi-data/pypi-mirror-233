# This file is placed in the Public Domain.
#
# pylint: disable=E0402,C0115,C0116.R0903


"reinforcement degrades performance"


from opv.objects import Object


def __dir__():
    return (
            'Censor',
            'doskip'
           )


class Censor(Object):

    skip = []


def skip(txt, skipping) -> bool:
    for skp in skipping:
        if skp in str(txt):
            return True
    return False


def doskip(txt):
    return skip(txt, Censor.skip)
