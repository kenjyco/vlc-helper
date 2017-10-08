from functools import partial
from collections import OrderedDict
from chloop import GetCharLoop
from vlc_helper import VLC


_vlc = VLC()

chfunc = OrderedDict([
    (' ', (_vlc.toggle_pause, 'pause/unpause')),
    ('s', (_vlc.screenshot, 'take a screenshot')),
    ('i', (_vlc.show_info, 'show info about currently playing file')),
    ('n', (_vlc.next, 'next file in playlist')),
    ('p', (_vlc.previous, 'previous file in playlist')),
    ('H', (partial(_vlc.seek, -30), 'rewind 30 seconds')),
    ('h', (partial(_vlc.seek, -5), 'rewind 5 seconds')),
    ('\x1b[D', (partial(_vlc.seek, -1), 'rewind 1 second (left arrow)')),
    ('L', (partial(_vlc.seek, 30), 'fast foward 30 seconds')),
    ('l', (partial(_vlc.seek, 5), 'fast foward 5 seconds')),
    ('\x1b[C', (partial(_vlc.seek, 1), 'fast foward 1 second (right arrow)')),
    ('K', (_vlc.killall, 'kill all VLC processes')),
])


class REPL(GetCharLoop):
    """A wrapper to control vlc video player with vim keybindings"""
    def seek(self, num):
        """Seek forward or backward"""
        _vlc.seek(float(num))

    def go(self, timestamp):
        """Jump to a particular timestamp"""
        _vlc.go(timestamp)


repl = REPL(chfunc_dict=chfunc, name='vlc', prompt='vlc-repl> ')
