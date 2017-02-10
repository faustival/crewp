#!/usr/bin/python3

import sys
from crewp.vasp.parsexml import ParseXML

if len(sys.argv) < 2:
    xmlfname = 'vasprun.xml'
else:
    xmlfname = sys.argv[1]

print('Parsing file: ', xmlfname)

xmlf = ParseXML(xmlfname)
xmlf.auto_creep()



