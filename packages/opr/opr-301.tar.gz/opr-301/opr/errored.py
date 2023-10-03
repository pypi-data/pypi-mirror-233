# This file is placed in the Public Domain.
#
# pylint: disable=E0402,C0103,C0116,W0612,W0622


"errors"


import traceback


from .censors import Censor, doskip
from .configs import Cfg


def __dir__():
    return (
            'Errors',
            'debug',
            'show'
           ) 


class Errors:

     errors = []
     output = None


def debug(txt):
    if "v" in Cfg.opts and Errors.output:
        if Errors.output and not doskip(txt):
            Errors.output(txt)


def show():
    for exc in Errors.errors:
        traceback.print_exception(
                                  type(exc),
                                  exc,
                                  exc.__traceback__
                                 )
