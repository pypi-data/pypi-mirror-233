# This file is placed in the Public Domain.
#
# pylint: disable=E0602,E0402,C0116


"locate"


from ..objects import fmt
from ..storage import files, find, long


def fnd(event):
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in files()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    clz = long(otype)
    if "." not in clz:
        for fnm in files():
            claz = fnm.split(".")[-1]
            if otype == claz.lower():
                clz = fnm
    nmr = 0
    for obj in find(clz, event.gets):
        event.reply(f"{nmr} {fmt(obj)}")
        nmr += 1
    if not nmr:
        event.reply("no result")
