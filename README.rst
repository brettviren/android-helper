Android Helper
==============

I have an HTC Inspire (aka Desire) phone which I have not yet rooted.
Thanks to AT&T's eminent wisdom they do not allow app stores besides
Android Market.  

Through their Android App Store, Amazon "sells" one app per day for
$0.00 which normally sells for more.  This is quite the inticing thing
but AT&T's policy of blocking 3rd party apps makes it a challeng to
enjoy Amazon's largess.

However, one can still install 3rd party apps by "sideloading" them,
that is installing them with the Android Debug Bridge (adb) that comes
with the Android SDK.  So, AT&T's policy is apparently something just
meant to annoy its customers.

It's straight-forward enough to use adb, but to simplify things,
Android Helper came to be.  The ``droid`` script bundles together some
tedious operations and presents a simple CLI to do common things.


Prerequisites
-------------

Installation of the Android SDK is an exercise left to the reader.
You will only need the "Android SDK Platform-tools" for the scripts.
After it has been done, edit the ``basedir`` variable at the top of
the ``droid`` script to reflect where it has been installed.

The ``zendroid`` script relies on the PyZenity package.  It can be
installed via::

  shell> sudo easy_install pyzenity


Installation
------------

It's just a script.  Copy or link it into your ``$PATH``.

::

  shell> ln -s /path/to/the/unpacked/android-helper/droid.py /somewhere/bin/droid
  shell> ln -s /path/to/the/unpacked/android-helper/zendroid.py /somewhere/bin/zendroid


Start the server
----------------

The Android Debug Bridge (``adb``) is used to do most of the work.  It
is a client-server pair.  The server usually needs to run as root to
overcome USB permissions.  If it isn't in root's path you will
probably have to specify the absolute path::

  shell> sudo /somewhere/bin/droid start-server

Most of the ``droid`` commands implemented require your device to be
configured for USB developer debugging turned on and to be connected
to your computers USB.  You only need to start the server once.


Installing Amazon Apps
----------------------

You will need to first download the Amazon App Store app by some means
and install it::

  shell> droid install Amazon_Appstore-release.apk

Then, on your phone, start the Appstore, select your app, wait for it
to download.  After downloading you will get an error message saying
that the app can not be installed.  **STOP**.  Don't clear the error
message yet.  Now plug in your phone to USB and do::

  shell> droid install_amazon

This will find all packages in Amazon's install cache on the phone
(``droid ls_amazon``), pull them down over USB to your current directory
(``droid pull_amazon rpath lpath``) and install (``droid install lpath``).

The app's ``.apk`` file will be left in the current directory.  It will be
named like ``vnz18515.apk``.  You can pull out a more useful name with::

  shell> droid package_name vnz18515.apk
  Enjoy Sudoku


Available Methods
-----------------

The general usage is::

  shell> droid command [command arguments]

Each command is just a function defined in the file.


