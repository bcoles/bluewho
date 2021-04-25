BlueWho
=======
**Description:** Information and notification of new discovered bluetooth devices

**Copyright:** 2009-2021 Fabio Castelli <muflone@muflone.com>

**License:** GPL-3+

**Source code:** https://github.com/muflone/bluewho

**Documentation:** http://www.muflone.com/bluewho

Information
-----------

The scan will automatically detect any visible device and for each one that was
detected a notification will be shown.

Each device found will be saved on the list with its name, type, address and
last seen date and time.

For each device a list of available Bluetooth services can be requested.

System Requirements
-------------------

* Python 3.x (developed and tested for Python 3.9)
* XDG library for Python 3
* GTK+3.0 libraries for Python 3
* GObject libraries for Python 3
* BlueZ library for Python 3
* Distutils library for Python 3 (usually shipped with Python distribution)

For the audio notification one of the following audio player is required:

 * canberra-gtk-play
 * aplay
 * paplay
 * mplayer

The application will scan the system and it will use the first player found.

Installation
------------

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python3 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python3 setup.py install --root NEW_PATH

Usage
-----

If the application is not installed please use:

    cd /path/to/folder
    python3 bluewho.py

If the application was installed simply use the bluewho command.
