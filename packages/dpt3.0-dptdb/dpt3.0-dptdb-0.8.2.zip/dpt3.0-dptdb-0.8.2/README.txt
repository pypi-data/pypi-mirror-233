==========================================
DPT database API wrappers built using SWIG
==========================================

.. contents::


Notice
======

`Github.com/RogerMarsh/dptdb`_ builds dpt3.0-dptdb wheels with `Build Tools for Visual Studio 2017`_.  It uses `Msys2`_ to extract and patch the C++ source code on Microsoft Windows.  Neither Build Tools for Visual Studio 2017 nor Msys2 is needed to run these dpt3.0-dptdb versions.

Development versions of dpt3.0-dptdb for 64-bit Pythons (\*-amd64.exe) can be built this way.


Description
===========

This package provides Python applications with the database API used by DPT.

DPT is a multi-user database system for Microsoft Windows.

The Python application can be as simple as a single-threaded process embedding the DPT API.

The package is available only as a source distribution.  It is built on Microsoft Windows in a `Msys2`_ environment using the mingw-w64-i686-gcc, mingw-w64-i686-python, and swig, ports.

Versions of dptdb earlier than 0.8 are built in a `MinGW`_ environment, but will not work at Python 3.8 or later even if a build succeeds.

The package can be used with the mingw-w64-i686-python port on Microsoft Windows.

The package cannot be used with any Python version installed by a Microsoft Python installer.

Setup will download the DPT API `source`_ and `documentation`_ zip files if an internet connection is available.

There is no separate documentation for Python.


Installation Instructions
=========================

   The package can be installed and used with the mingw-w64-i686-python port in a `Msys2`_ environment on Microsoft Windows.

   Build dependencies

      * `Python`_ 2.7 or later 
      * `SWIG`_ 4.0.1 or later
      * `Msys2`_

      Download and install the `Msys2`_ environment.

      Follow the `Msys2`_ instructions to install Msys2.

      Install SWIG and Python using the pacman utility.

   Install the package by typing

       python setup.py install --user

   at the command prompt of a MINGW32 shell with setup.py in the current directory.

   Runtime dependencies

   * `Msys2`_ environment with the mingw-w64-i686-python port used to build dptdb.

A directory named like dpt3.0_dptdb-0.5-py2.7.egg is put in site-packages by the install command.  The name means version 0.5 of dptdb for Python 2.7 wrapping version 3.0 of the DPT API.  This directory contains the dptdb and EGG-INFO directories.

The DPT documentation zip file is in the source distribution.


Sample code
===========

The dptdb/test directory contains a simple application which populates a database, using some contrived data, and does some simple data retrievals.

This can be run on Microsoft Windows by typing

   python pydpt-test.py

at the command prompt of a MINGW32 shell with pydpt-test.py in the current directory.

You may need to use '<path to python>/python pydpt-test.py' if several versions of Python are installed.


The sample application offers seven options which create databases with different numbers of records.  Each record has 6 fields and all fields are indexed.

   One option, called normal, adds 246,625 records to a database in a 16 Mb file in about 3.33 minutes with transaction backout enabled.

   The shortest option adds 246,625 records to a database in a 16 Mb file in about 0.6 minutes with transaction backout disabled.

   The longest option adds 7,892,000 records to a database in a 526 Mb file in about 18.75 minutes with transaction backout disabled.

The figures are for a 2Gb 667MHz memory, 1.8GHz CPU, solid state drive, Microsoft Windows XP installation.


Restrictions
============

It is not known if dptdb is now usable in a `Msys2`_ environment under `Wine`_, or if the restrictions which affected the old versions built in a `MinGW`_ environment would be relevant.


Notes
=====

This package is built from `DPT_V3R0_DBMS.ZIP`_, a recent DPT API source code distribution, by default.

You will need the `DPT API documentation`_ to use this package.  This is included as `DBAPI.html`_ in DPT_V3R0_DOCS.ZIP.

The DPT documentation zip file is in a directory named like C:/Python27/Lib/site-packages/dpt3.0_dptdb-0.5-py2.7.egg/dptdb, using the example at the end of `Installation Instructions`_.

A _dptapi.pyd built for Python 2.7 will work only on Python 2.7 and so on. 

The `DPT API distribution`_ contains independent scripts and instructions to build dptdb mentioning much earlier versions of the build dependencies.


.. _DPT API documentation: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _documentation: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _DBAPI.html: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _relnotes_V2RX.html: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _DPT_V3R0_DBMS.ZIP: http://solentware.co.uk/files/DPT_V3R0_DBMS.ZIP
.. _DPT API distribution: http://solentware.co.uk/files/DPT_V3R0_DBMS.ZIP
.. _source: http://solentware.co.uk/files/DPT_V3R0_DBMS.ZIP
.. _Msys2: http://msys2.org
.. _Python: https://python.org
.. _SWIG: http://swig.org
.. _MinGW: http://mingw.org
.. _Wine: https://winehq.org
.. _Github.com/RogerMarsh/dptdb: https://github.com/RogerMarsh/dptdb
.. _Build Tools for Visual Studio 2017: https://visualstudio.microsoft.com/vs/older-downloads/
