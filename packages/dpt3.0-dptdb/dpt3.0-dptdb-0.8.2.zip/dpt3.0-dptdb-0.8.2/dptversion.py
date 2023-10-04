# dpt_version.py
# Copyright 2013 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Utility to create version information module for dptdb package.

This script expects to be run in an MSYS shell.

"""

import sys
import os
import re

_DPTDB_VERSION = '0.8.2'


def record_dpt_and_dptdb_versions():
    """Extract DPT API version number from parmref.cpp

    This method is adapted from dptversion.py in the DPT API distribution.
    It is not appropriate to share the code between the packages.  In other
    words to amend dptversion.py to cope with this module's needs.

    """
    version_line = re.compile(''.join((
        '\s*StoreEntry.*VERSDPT.*?(?P<version>((\d+\.)*\d+))')))
    version = '0.0'
    f = open(os.path.join('source', 'parmref.cpp'), 'r')
    for t in f.readlines():
        vl = version_line.match(t)
        if vl is not None:
            version = str(vl.group('version'))
            break
    f.close()
    version = ''.join(('_dpt_version = ', "'", version, "'"))
    dptdb_version = ''.join(('_dptdb_version = ', "'", _DPTDB_VERSION, "'"))
    vs = {'_Swig': '', '_MinGW': '', '_Python': ''}
    version_file = os.path.join('..', 'version.py')
    if os.path.isfile(version_file):
        for nv in open(version_file):
            nvl = [s.strip() for s in nv.split('=')]
            if len(nvl) == 1:
                continue
            n, v = nvl
            if n == '_Swig':
                vs['_Swig'] = v
            elif n == '_MinGW':
                vs['_MinGW'] = v
            elif n == '_Python':
                vs['_Python'] = v
        os.remove(version_file)
    f = open(version_file, 'w')
    try:
        f.write(version)
        f.write(os.linesep)
        f.write(dptdb_version)
        f.write(os.linesep)
        for k, v in vs.items():
            if v:
                f.write(' = '.join((k , v)))
                f.write(os.linesep)
    finally:
        f.close()


def remove_Python_and_SWIG_versions():
    """Remove Python and SWIG version information from version.py.

    This allows rebuilds with different Python and SWIG versions.

    """
    version_file = os.path.join('version.py')
    rv = []
    if os.path.isfile(version_file):
        for nv in open(version_file):
            nvl = [s.strip() for s in nv.split('=')]
            if len(nvl) == 1:
                if len(nvl[0]):
                    rv.append(nv)
                continue
            n, v = nvl
            if n == '_Swig':
                continue
            elif n == '_Python':
                continue
            rv.append(nv)
        os.remove(version_file)
        f = open(version_file, 'w')
        try:
            for l in rv:
                f.write(l)
        finally:
            f.close()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        record_dpt_and_dptdb_versions()
    elif sys.argv[1] == 'clean_swig':
        remove_Python_and_SWIG_versions()
    elif sys.argv[1] == 'clean_python_version':
        remove_Python_and_SWIG_versions()
    elif sys.argv[1] == 'clean_all_pythons':
        remove_Python_and_SWIG_versions()
