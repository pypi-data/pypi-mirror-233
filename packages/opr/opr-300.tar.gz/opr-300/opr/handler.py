# This file is placed in the Public Domain.
#
# pylint: disable=E0402,C0115,C0116,W0718,W0702,W0212


"runtime"


import inspect
import os
import queue
import threading
import time
import _thread


from opv.objects import Default, Object


from opr.brokers import say
from opr.errored import Errors
from opr.parsers import parse
from opr.threads import launch


def __dir__():
    return (
            'EVent',
            'Handler',
            'command',
            'mods'
           )


SLEEP = 1.0


class Event(Default):

    __slots__ = ('_ready', "_thr")

    def __init__(self, *args, **kwargs):
        Default.__init__(self, *args, **kwargs)
        self._ready = threading.Event()
        self.channel = ""
        self.orig = ""
        self.result = []
        self.txt = ""
        self.type = "command"

    def ready(self):
        self._ready.set()

    def reply(self, txt) -> None:
        self.result.append(txt)

    def show(self) -> None:
        for txt in self.result:
            say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()


class Handler:

    cmds = {}

    def __init__(self):
        self.cbs = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()

    @staticmethod
    def add(func):
        Handler.cmds[func.__name__] = func

    def announce(self, txt):
        pass

    def dosay(self, channel, txt):
        pass

    def event(self, txt):
        evt = Event()
        evt.txt = txt
        evt.orig = object.__repr__(self)
        return evt

    def forever(self):
        while not self.stopped.is_set():
            try:
                time.sleep(SLEEP)
            except:
                _thread.interrupt_main()

    def dispatch(self, evt):
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        try:
            evt._thr = launch(func, evt)
        except Exception as ex:
            exc = ex.with_traceback(ex.__traceback__)
            Errors.errors.append(exc)
            evt.ready()

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                self.dispatch(self.poll())
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self) -> Event:
        return self.queue.get()

    @staticmethod
    def scan(mod) -> None:
        for key, cmd in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Handler.add(cmd)

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()


def command(evt):
    parse(evt, evt.txt)
    func = Handler.cmds.get(evt.cmd, None)
    if not func:
        evt.ready()
        return
    try:
        func(evt)
        evt.show()
    except Exception as ex:
        exc = ex.with_traceback(ex.__traceback__)
        Errors.errors.append(exc)
    evt.ready()


def mods(path):
    res = []
    for fnm in os.listdir(path):
        if fnm.endswith("~"):
            continue
        if not fnm.endswith(".py"):
            continue
        if fnm in ["__main__.py", "__init__.py"]:
            continue
        res.append(fnm[:-3])
    return sorted(res)
