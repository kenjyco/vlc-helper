__all__ = ['VLC', 'vlcstart_precise', 'play_many']


import subprocess
import re
import os
import time
import urllib
import vlc_helper as vh
import input_helper as ih
from functools import partial
from pprint import pprint
from bg_helper import SimpleBackgroundTask
try:
    import dbus
except ImportError:
    pass


class VLC(object):
    """A limited CLI interface to a running vlc session

    http://askubuntu.com/questions/405931
    http://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html
    """
    def __init__(self):
        pass

    def _refresh_bus(self):
        """Get a new bus object for vlc and set internal vars"""
        bus = dbus.SessionBus()
        try:
            self._bus_obj = bus.get_object('org.mpris.MediaPlayer2.vlc', '/org/mpris/MediaPlayer2')
        except dbus.DBusException:
            vlcstart_precise(background=True)
            time.sleep(1)
            try:
                self._bus_obj = bus.get_object('org.mpris.MediaPlayer2.vlc', '/org/mpris/MediaPlayer2')
            except dbus.DBusException:
                raise Exception('vlc is not running')

        self._properties_interface = dbus.Interface(self._bus_obj, 'org.freedesktop.DBus.Properties')
        self._player = dbus.Interface(self._bus_obj, 'org.mpris.MediaPlayer2.Player')
        self._prop_get = partial(self._properties_interface.Get, 'org.mpris.MediaPlayer2.Player')
        self._prop_set = partial(self._properties_interface.Set, 'org.mpris.MediaPlayer2.Player')

    def _get(self, name):
        """Return the value of a `MediaPlayer2.Player` property"""
        try:
            return self._prop_get(name)
        except (dbus.DBusException, AttributeError):
            self._refresh_bus()
            return self._prop_get(name)

    def _set(self, name, value):
        """Set a `MediaPlayer2.Player` property"""
        try:
            return self._prop_set(name, value)
        except (dbus.DBusException, AttributeError):
            self._refresh_bus()
            return self._prop_set(name, value)

    def _method(self, name, *args):
        """Run a `MediaPlayer2.Player` method"""
        try:
            if args:
                cmd = partial(getattr(self._player, name), *args)
            else:
                cmd = getattr(self._player, name)
            cmd()
        except (AttributeError, dbus.exceptions.DBusException):
            self._refresh_bus()
            if args:
                cmd = partial(getattr(self._player, name), *args)
            else:
                cmd = getattr(self._player, name)
            cmd()

    @property
    def _metadata(self):
        return self._get('Metadata')

    @property
    def _path(self):
        path = self._metadata.get('xesam:url')
        if not path:
            return ''
        return urllib.parse.unquote_plus(str(path))

    @property
    def position(self):
        """Return current video position (in seconds, not microseconds)"""
        return int(self._get('Position')) / 1000000.0

    @property
    def filename(self):
        return os.path.basename(self._path)

    @property
    def dirname(self):
        try:
            return os.path.dirname(self._path).split('://')[1]
        except IndexError:
            return ''

    @property
    def window_title(self):
        """Return name of vlc window, (to be passed to ImageMagick's `import` cmd)

        See: `-window` option in `man import`
        """
        rx = re.compile(r'^(?:\S+\s+){3}(.*)$')
        try:
            output = subprocess.check_output('wmctrl -l | grep "VLC media player"', shell=True)
            output = output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return ''

        output = output.split('\n')[0]
        title = rx.match(output).group(1)
        return title

    @property
    def info(self):
        return {
            'filename': self.filename,
            'dirname': self.dirname,
            'position': self.position,
            'window_title': self.window_title
        }

    def show_info(self, fmt='{position} {dirname}/{filename}'):
        """Display formatted string from self.info dict"""
        print(fmt.format(**self.info))

    def toggle_pause(self):
        self._method('PlayPause')

    def seek(self, val):
        """Seek forward or backward specified number of seconds"""
        self._method('Seek', (val * 1000000.0))

    def go(self, timestamp):
        """Jump to timestamp in the current file (wrapper to self.seek)"""
        seconds = ih.timestamp_to_seconds(timestamp)
        if seconds is None:
            return
        self.seek(seconds - int(self.position))

    def next(self):
        self._method('Next')

    def previous(self):
        self._method('Previous')

    def _screenshot(self):
        """Take a screenshot and include file position in output filename"""
        if not self.dirname:
            return
        outfile_base, ext = os.path.splitext(self.filename)
        outfile_name = 'screenshot--{}--{}.png'.format(
            outfile_base,
            str(self.position).rjust(12, '0')      # zero-pad the float as a string
        )
        outfile = os.path.join(self.dirname, outfile_name)
        cmd = 'import -window {} {}'.format(repr(self.window_title), repr(outfile))
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            vh.logger.error(e.output)
        return outfile

    def screenshot(self):
        SimpleBackgroundTask(self._screenshot)

    def killall(self):
        def get_pids():
            try:
                output = subprocess.check_output(
                    'pgrep vlc',
                    stderr=subprocess.STDOUT,
                    shell=True
                )
            except subprocess.CalledProcessError as e:
                return []
            else:
                return output.decode('utf-8').split('\n')[:-1]

        pids = get_pids()
        vh.logger.debug('About to kill PIDS {}'.format(repr(pids)))
        for pid in pids:
            try:
                output = subprocess.check_output(
                    'kill {}'.format(pid),
                    stderr=subprocess.STDOUT,
                    shell=True
                )
            except subprocess.CalledProcessError as e:
                vh.logger.error(e.output)

        time.sleep(1)
        for pid in get_pids():
            try:
                output = subprocess.check_output(
                    'kill -9 {}'.format(pid),
                    stderr=subprocess.STDOUT,
                    shell=True
                )
            except subprocess.CalledProcessError as e:
                vh.logger.error(e.output)


def vlcstart_precise(filename='', starttime='', stoptime='', background=False):
    if not os.getenv('DISPLAY'):
        vh.logger.warning('not connected to a DISPLAY')
        return
    if filename:
        fullpath = os.path.abspath(os.path.expanduser(filename))
        starttime = ih.timestamp_to_seconds(starttime) or 0
        stoptime = ih.timestamp_to_seconds(stoptime) or 0
        if stoptime:
            _cmd = 'vlc --fullscreen --start-time {} --stop-time {} {} &>/dev/null'.format(starttime, stoptime, repr(str(fullpath)))
        else:
            _cmd = 'vlc --fullscreen --start-time {} {} &>/dev/null'.format(starttime, repr(str(fullpath)))
    else:
        _cmd = 'vlc &>/dev/null'

    cmd = partial(subprocess.check_output, _cmd, stderr=subprocess.STDOUT, shell=True)
    if not background:
        try:
            cmd()
        except subprocess.CalledProcessError as e:
            vh.logger.error(e.output)
    else:
        SimpleBackgroundTask(cmd)


def play_many(*filenames, background=False):
    if not os.getenv('DISPLAY'):
        vh.logger.warning('not connected to a DISPLAY')
        return
    if filenames:
        _cmd = 'vlc --fullscreen {} &>/dev/null'.format(
            ' '.join([repr(x) for x in filenames])
        )
    else:
        _cmd = 'vlc &>/dev/null'

    cmd = partial(subprocess.check_output, _cmd, stderr=subprocess.STDOUT, shell=True)
    if not background:
        try:
            cmd()
        except subprocess.CalledProcessError as e:
            vh.logger.error(e.output)
    else:
        SimpleBackgroundTask(cmd)
