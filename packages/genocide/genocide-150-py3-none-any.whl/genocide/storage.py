# This file is placed in the Public Domain.
#
# pylint: disable=C0112,C0115,C0116,W0105,R0903,E0402,C0209,R1710


"storage"


import datetime
import inspect
import os
import pathlib
import time
import uuid
import _thread


from .objects import Object, fqn, read, search, update, write


def  __dir__():
    return (
            'Storage',
            'fetch',
            'find',
            'fns',
            'long',
            'path',
            'read',
            'store',
            'sync',
            'write'
           )


lock = _thread.allocate_lock()


class Storage:

    classes = {}
    workdir = ""

    @staticmethod
    def add(clz):
        if not clz:
            return
        name = str(clz).split()[1][1:-2]
        Storage.classes[name] = clz

    @staticmethod
    def scan(mod) -> None:
        for key, clz in inspect.getmembers(mod, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)


def fetch(obj, pth):
    pth2 = store(pth)
    read(obj, pth2)
    obj.__fnm__ = strip(pth)


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x.__fnm__)
                   )
    if result:
        inp = result[-1]
        update(obj, inp)
        obj.__fnm__ = inp.__fnm__


def sync(obj, pth=None):
    pth = pth or obj.__fnm__
    if not pth:
        pth = ident(obj)
    pth2 = store(pth)
    write(obj, pth2)
    obj.__fnm__ = pth
    return pth


"utility"


def cdir(pth) -> None:
    if not pth.endswith(os.sep):
        pth = os.path.dirname(pth)
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def fntime(daystr) -> float:
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    else:
        timed = 0
    return timed


def files() -> []:
    return os.listdir(store())


def find(mtc, selector=None) -> []:
    if selector is None:
        selector = {}
    clz = long(mtc)
    for fnm in reversed(sorted(fns(clz), key=fntime)):
        obj = Object()
        fetch(obj, fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        yield obj


def fns(mtc) -> []:
    dname = ''
    pth = store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            dname = sorted(dirs)[-1]
            if dname.count('-') == 2:
                ddd = os.path.join(rootdir, dname)
                fls = sorted(os.listdir(ddd))
                if fls:
                    yield strip(os.path.join(ddd, fls[-1]))


def ident(obj) -> str:
    return os.path.join(
                        fqn(obj),
                        str(uuid.uuid4().hex),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def laps(seconds, short=True) -> str:
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if years:
        txt += f"{years}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if nrdays and short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def long(name):
    split = name.split(".")[-1].lower()
    res = name
    for named in Storage.classes:
        if split in named.split(".")[-1].lower():
            res = named
            break
    return res


def path(pth):
    if not pth:
        pth = ""
    assert Storage.workdir
    pth2 =  os.path.join(Storage.workdir, pth)
    cdir(pth2)
    return pth2


def spl(txt) -> []:
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def store(pth=""):
    assert Storage.workdir
    pth = os.path.join(Storage.workdir, "store", pth)
    cdir(pth)
    return pth


def strip(pth) -> str:
    return os.sep.join(pth.split(os.sep)[-4:])
