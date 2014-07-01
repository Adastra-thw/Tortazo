#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher


def on_message(number):
    print 'In the handler'
    if not number == 762:
        raise SystemExit('wx_pubsub_kwargs failed.')


Publisher.subscribe(on_message, 'topic.subtopic')
Publisher.sendMessage('topic.subtopic', number=762)
