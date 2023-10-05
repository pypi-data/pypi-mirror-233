# This file is placed in the Public Domain.
#
# pylint: disable=E0402,C0116


"list of commands"


from ..runtime import Handler


def cmd(event):
    event.reply(",".join(sorted(Handler.cmds)))
