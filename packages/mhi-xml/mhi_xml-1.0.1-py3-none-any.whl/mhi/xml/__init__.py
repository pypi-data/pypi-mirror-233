"""
Library for reading/updating various kinds of MHI-specific XML files
"""

_VERSION = (1, 0, 1)
_TYPE = 'f0'

VERSION = '{0}.{1}.{2}'.format(*_VERSION, _TYPE)
VERSION_HEX = int.from_bytes((*_VERSION, int(_TYPE, 16)), byteorder='big')
