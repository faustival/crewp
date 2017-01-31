#!/usr/bin/python3

import sys
from crewp.vasp.parsexml import get_bornchg, auto_creep

if len(sys.argv) < 2:
    xmlfname = 'vasprun.xml'
else:
    xmlfname = sys.argv[1]

print('Parsing file: ', xmlfname)

#get_bornchg(xmlfname)
auto_creep(xmlfname)



