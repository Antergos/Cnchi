#!/bin/python

try:
    import xml.etree.cElementTree as eTree
except ImportError as err:
    import xml.etree.ElementTree as eTree

try:
    xml_tree = eTree.parse("/usr/share/cnchi/data/packages.xml")
except eTree.ParseError as err:
    lineno, column = err.position
    err.msg = '{}\n{}\n{}'.format(err, lineno, column)
    raise
