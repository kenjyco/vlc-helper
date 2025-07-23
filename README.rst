A streamlined interface for precise video control and screenshot capture
with VLC media player on Linux systems, built on the
`chloop <https://github.com/kenjyco/chloop>`__ REPL framework. This
library provides D-Bus integration for real-time VLC control and
vim-style keyboard navigation designed for interactive video analysis
and content review workflows.

**Linux-only requirements:** This library uses D-Bus for VLC
communication, ImageMagick for screenshot capture, and ``wmctrl`` for
window management, making it compatible with Linux desktop environments
only.

The core philosophy emphasizes **precision and workflow optimization**
for users who need frame-accurate video navigation, timestamped
screenshot capture, and immediate keyboard control during active video
review. Rather than wrestling with VLC’s complex interface during
detailed video work, vlc-helper reduces cognitive overhead by providing
instant keyboard shortcuts and direct player control for essential
playback functions.

**Who benefits from this library:** - Video editors and content creators
reviewing footage frame-by-frame - Researchers analyzing video content
with precise timestamp requirements - Educators creating timestamped
video materials and screenshots - Quality assurance professionals
testing video applications - Content reviewers needing rapid navigation
and screenshot workflows - Anyone requiring precise video navigation
during active viewing sessions

Install
-------

Install system requirements for ``dbus-python`` package

::

   sudo apt-get install -y pkg-config libdbus-1-dev libdbus-glib-1-dev

Install with ``pip``

::

   pip install vlc-helper

QuickStart
----------

The ``vlc-repl`` and ``myvlc`` scripts are provided.

.. code:: bash

   # Start VLC with precise timestamp control
   myvlc video.mp4 "1h23m45s" "1h25m30s"  # Play from 1:23:45 to 1:25:30

   # Or start the interactive controller for any running VLC
   vlc-repl

**Interactive Controls:** - ``space`` - pause/unpause - ``s`` - take
screenshot with timestamp in filename - ``i`` - show current file info
and position - ``h``/``l`` - seek backward/forward (5 seconds) -
``H``/``L`` - seek backward/forward (30 seconds) - ``←``/``→`` - seek
backward/forward (1 second, arrow keys) - ``n``/``p`` - next/previous
file in playlist - ``K`` - kill all VLC processes

**Colon Commands:** - ``:seek 15`` - seek forward 15 seconds -
``:go 1h23m45s`` - jump to specific timestamp

**What you gain:** Transform VLC from a general media player into a
precision video analysis tool during active viewing. Capture perfectly
timestamped screenshots, navigate to exact moments with single
keystrokes, and maintain focus on content analysis rather than interface
navigation. Essential for workflows requiring frame-accurate video
review.

API Overview
------------

High-Level Video Control
~~~~~~~~~~~~~~~~~~~~~~~~

Interactive REPL Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **``repl``** - Pre-configured interactive controller for running VLC
   instances

   -  Inherits from GetCharLoop for single-keystroke efficiency
   -  ``chfunc_dict``: Ordered dictionary mapping keys to VLC control
      functions
   -  ``name``: Collection name for logging (‘vlc’)
   -  ``prompt``: Display prompt (‘vlc-repl>’)
   -  Returns: Interactive video control session
   -  Internal calls: GetCharLoop.__init__, VLC() instance methods

Precise Video Launching
^^^^^^^^^^^^^^^^^^^^^^^

-  **``vlcstart_precise(filename='', starttime='', stoptime='', background=False)``**
   - Launch VLC with exact timing control

   -  ``filename``: Video file path (supports ~ expansion and relative
      paths)
   -  ``starttime``: Start timestamp in formats like ‘1h23m45s’,
      ‘2:15:30’, ‘300s’
   -  ``stoptime``: Optional end timestamp (VLC stops playback
      automatically)
   -  ``background``: If True, launch without blocking using
      SimpleBackgroundTask
   -  Returns: None (launches VLC process for interactive control)
   -  Internal calls: ih.timestamp_to_seconds, SimpleBackgroundTask

-  **``play_many(*filenames, background=False)``** - Launch VLC with
   multiple files in playlist

   -  ``*filenames``: Multiple video file paths
   -  ``background``: If True, launch without blocking
   -  Returns: None (launches VLC with playlist for interactive control)
   -  Internal calls: SimpleBackgroundTask

VLC Player Control
~~~~~~~~~~~~~~~~~~

VLC Class - D-Bus Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **``VLC()``** - D-Bus interface for controlling running VLC player
   instances

   -  Auto-connects to VLC via MPRIS (Media Player Remote Interfacing
      Specification)
   -  Handles connection failures with automatic VLC startup and
      reconnection
   -  Returns: VLC control object with real-time playback and metadata
      access
   -  Internal calls: vlcstart_precise()

Playback State Management
^^^^^^^^^^^^^^^^^^^^^^^^^

-  **``VLC.toggle_pause()``** - Toggle play/pause state

   -  Returns: None (changes playback state immediately)
   -  Internal calls: None

-  **``VLC.next()``** - Skip to next file in playlist

   -  Returns: None (advances to next track)
   -  Internal calls: None

-  **``VLC.previous()``** - Skip to previous file in playlist

   -  Returns: None (goes to previous track)
   -  Internal calls: None

Navigation and Seeking
^^^^^^^^^^^^^^^^^^^^^^

-  **``VLC.seek(val)``** - Relative seeking forward or backward

   -  ``val``: Number of seconds (positive=forward, negative=backward)
   -  Returns: None (updates playback position instantly)
   -  Internal calls: None

-  **``VLC.go(timestamp)``** - Jump to absolute position in video

   -  ``timestamp``: Target time in formats like ‘1h23m45s’, ‘2:15:30’,
      ‘300s’
   -  Returns: None (seeks to exact position)
   -  Internal calls: ih.timestamp_to_seconds, VLC.seek()

Video Information and Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **``VLC.position``** (property) - Current playback position in
   seconds

   -  Returns: Float representing current video position
   -  Internal calls: None

-  **``VLC.filename``** (property) - Current video filename without path

   -  Returns: String basename of currently playing file
   -  Internal calls: None

-  **``VLC.dirname``** (property) - Directory path of current video

   -  Returns: String directory path (handles file:// URLs)
   -  Internal calls: None

-  **``VLC.window_title``** (property) - VLC window title for external
   tool targeting

   -  Returns: String window title suitable for ImageMagick import
      command (uses wmctrl)
   -  Internal calls: None

-  **``VLC.info``** (property) - Combined metadata dictionary

   -  Returns: Dict with ‘filename’, ‘dirname’, ‘position’,
      ‘window_title’
   -  Internal calls: VLC.position, VLC.filename, VLC.dirname,
      VLC.window_title

-  **``VLC.show_info(fmt='{position} {dirname}/{filename}')``** -
   Display formatted video information

   -  ``fmt``: Format string template for display
   -  Returns: None (prints current video state)
   -  Internal calls: VLC.info

Screenshot Capture
^^^^^^^^^^^^^^^^^^

-  **``VLC.screenshot()``** - Capture current frame with timestamped
   filename

   -  Returns: None (saves PNG with format:
      screenshot–filename–timestamp.png using ImageMagick)
   -  Internal calls: VLC._screenshot(), SimpleBackgroundTask

-  **``VLC.killall()``** - Force terminate all VLC processes

   -  Returns: None (kills processes with escalating signals)
   -  Internal calls: None

REPL Interactive Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~

REPL Class - Interactive Controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  **``REPL(chfunc_dict, name='vlc', prompt='vlc-repl> ')``** -
   Interactive video controller with vim-style keybindings

   -  ``chfunc_dict``: Ordered dictionary mapping keys to VLC control
      functions
   -  ``name``: Collection name for logging
   -  ``prompt``: Display prompt
   -  Inherits from GetCharLoop for single-keystroke efficiency
   -  Returns: Interactive video control session
   -  Internal calls: GetCharLoop.__init_\_

REPL Command Methods
^^^^^^^^^^^^^^^^^^^^

-  **``REPL.seek(num)``** - Seek by specified number of seconds (colon
   command)

   -  ``num``: Seconds to seek (string converted to float)
   -  Returns: None (calls VLC.seek for immediate response)
   -  Internal calls: VLC.seek()

-  **``REPL.go(timestamp)``** - Jump to specific timestamp (colon
   command)

   -  ``timestamp``: Target time in supported formats
   -  Returns: None (calls VLC.go for precise navigation)
   -  Internal calls: VLC.go()
