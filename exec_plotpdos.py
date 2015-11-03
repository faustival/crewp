#! /usr/bin/python3

import os
from atom import Atom

slablist = [
{ 'sys':'au3pd', 'atomlist':[[12,'Au',['d']],[13,'Pd',['d']]], },
]

rootdir = '/home/jinxi/pwjobs/cyan_ads/'

for slab in slablist:
    os.chdir(rootdir + slab['sys'])
    for atom in slab['atomlist']:
        atm = Atom(atom[0],atom[1])
        atm.get_ldos('plt', atom[2])



