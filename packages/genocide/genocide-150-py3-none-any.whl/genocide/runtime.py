# This file is placed in the Public Domain.
#
# pylint: disable=E0402,C0115,C0116,W0718,W0702,W0212,C0411,W0613,R0903,E1102
# pylint: disable=C0103


"runtime"


import inspect
import io
import os
import queue
import threading
import traceback
import _thread


from .objects import Default, Object
from .storage import Storage, spl
from .threads import launch


def __dir__():
    return (
            'Broadcast',
            'Broker',
            'Cache',
            'Censor',
            'Errors',
            'Event',
            'Handler',
            'command',
            'mods'
           )


Cfg = Default()
output = None


def debug(txt):
    if output is None:
        return
    if Censor.skip(txt):
        return
    if "v" in Cfg.opts:
        output(txt)


class Broker:

    objs = []

    @staticmethod
    def add(obj) -> None:
        Broker.objs.append(obj)

    @staticmethod
    def byorig(orig):
        for obj in Broker.objs:
            if object.__repr__(obj) == orig:
                return obj
        return None

    @staticmethod
    def bytype(typ):
        for obj in Broker.objs:
            if typ in object.__repr__(obj):
                return obj
        return None

    @staticmethod
    def remove(obj) -> None:
        try:
            Broker.objs.remove(obj)
        except ValueError:
            pass


class BroadCast:

    @staticmethod
    def announce(txt):
        for obj in Broker.objs:
            obj.announce(txt)

    @staticmethod
    def say(orig, channel, txt):
        bot = Broker.byorig(orig)
        if not bot:
            return
        bot.dosay(channel, txt)


class Cache(Default):

    cache = {}

    @staticmethod
    def size(chan):
        if chan in Cache.cache:
            return len(Cache.cache.get(chan, []))
        return 0


class Censor(Object):

    words = []

    @staticmethod
    def skip(txt) -> bool:
        for skp in Censor.words:
            if skp in str(txt):
                return True
        return False


class Errors(Object):

    errors = []

    @staticmethod
    def format(exc):
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            res += line + "\n"
        return res

    @staticmethod
    def handle(exc):
        output(Errors.format(exc))

    @staticmethod
    def show():
        for exc in Errors.errors:
            Errors.handle(exc)


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
            BroadCast.say(self.orig, self.channel, txt)

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
        self.end = threading.Event()

    @staticmethod
    def add(func):
        Handler.cmds[func.__name__] = func

    def event(self, txt):
        evt = Event()
        evt.txt = txt
        evt.orig = object.__repr__(self)
        return evt

    def forever(self):
        self.stopped.wait()

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

    def put(self, evt):
        self.queue.put_nowait(evt)

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


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)
        Broker.add(self)

    def announce(self, txt):
        self.raw(txt)

    def dosay(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        pass


def command(evt):
    parse(evt)
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


def parse(obj, txt=None) -> None:
    args = []
    obj.args = obj.args or []
    obj.cmd = obj.cmd or ""
    obj.gets = obj.gets or {}
    obj.hasmods = obj.hasmod or False
    obj.mod = obj.mod or ""
    obj.opts = obj.opts or ""
    obj.result = obj.reult or []
    obj.sets = obj.sets or {}
    obj.otxt = txt or obj.txt or ""
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            obj.sets[key] = value
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            obj.gets[key] = value
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def scan(pkg, modnames="", initer=False, dowait=False) -> []:
    if not pkg:
        return []
    inited = []
    scanned = []
    threads = []
    for modname in spl(modnames):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        scanned.append(modname)
        Handler.scan(module)
        Storage.scan(module)
        if initer:
            try:
                module.init
            except AttributeError:
                continue
            inited.append(modname)
            debug(f"starting {modname}")
            threads.append(launch(module.init, name=f"init {modname}"))
    if dowait:
        for thread in threads:
            thread.join()
    return inited
