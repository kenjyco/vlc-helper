## Warning

This is **Linux only** as D-BUS does not work on Mac.

You must have the following system packages installed

- `vlc`
- `imagemagick` (to take screenshots)
- `wmctrl` (to determine window name)

## Install

Install system requirements for `dbus-python` package

```
% sudo apt-get install -y pkg-config libdbus-1-dev libdbus-glib-1-dev
```

Install with `pip`

```
% pip3 install vlc-helper
```

## Usage

The `vlc-repl` and `myvlc` scripts are provided

```
% venv/bin/vlc-repl --help
Usage: vlc-repl [OPTIONS]

  Start a REPL to control VLC media player

Options:
  --help  Show this message and exit.

% venv/bin/myvlc --help
Usage: myvlc [OPTIONS] [FILENAME] [STARTTIME] [STOPTIME]

  Start filename at specific start time (and/or end at specific end time)

Options:
  --help  Show this message and exit.

```
