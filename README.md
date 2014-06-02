adb_batch_uninstaller
=====================

Python script to batch uninstall a bunch of Android applications from a device using ADB.

Typical use case is to have several applications to uninstall frequently and at the same time, e.g. an application and its test or sample application, or its different flavors.

Settings
--------

Currently the applications to uninstall are set within in a constant at the head of the script, `UNINSTALL_APP_PREFIXES`.
As the name suggests this is a prefix so any package which name *starts with* any these strings will be uninstalled.

Usage
-----

The only option it currently accepts is
- `-s <DEVICE>` which is directly passed to `adb` to specify the device to uninstall from if several are available. See `adb` documentation for details.

Installation
------------

`python3` and `adb` are required and have to be on the `$PATH` of the executing shell.
Then just make the script executable and run it:

    $ chmod u+x ./adb_batch_uninstaller.py
    $ ./adb_batch_uninstaller.py

