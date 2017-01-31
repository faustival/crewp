#! /usr/bin/python3

import lxml.etree as etr
import numpy as np

def get_latvecs(fname='vasprun.xml'):
    pass

def get_rlx_traj_pos(fname='vasprun.xml'):
    xmltree = etr.parse(fname)
    elem_position_list = xmltree.xpath('//calculation/structure/varray[@name="positions"]')
    rlx_pos3 = [] # len = number of steps
    for elem_position in elem_position_list:
        rlx_pos3_step = [] # len = number of atoms
        for elem in elem_position:
            rlx_pos3_step.append( [ float(a) for a in elem.text.split() ] )
        rlx_pos3.append(rlx_pos3_step)
    return rlx_pos3

def get_rlx_traj_latvec(fname='vasprun.xml'):
    xmltree = etr.parse(fname)
    elem_latvec_list = xmltree.xpath('//calculation/structure/crystal/varray[@name="basis"]')
    rlx_latvec = [] # len = number of steps
    for elem_latvec in elem_latvec_list :
        rlx_latvec_step = [] # len = 3        
        for elem in elem_latvec:
            rlx_latvec_step.append( [ float(a) for a in elem.text.split() ] )
        rlx_latvec.append(rlx_latvec_step)
    return rlx_latvec

def get_rlx_traj_forc(fname='vasprun.xml'):
    pass

def get_vib(fname='vasprun.xml'):
    pass

def auto_creep(fname='vasprun.xml'):
    xmltree = etr.parse(fname)
    '''
    # Get required parameters for auto creep:
    #   IBRION, ISIF
    '''
    elem_ibrion, = xmltree.xpath('//parameters/separator[@name="ionic"]/i[@name="IBRION"]') # don't parse <incar> tag
    elem_isif, = xmltree.xpath('//parameters/separator[@name="ionic"]/i[@name="ISIF"]') # don't parse <incar> tag
    ibrion = int(elem_ibrion.text)
    isif = int(elem_isif.text)
    if 1 <= ibrion <= 3:
        if 0 <= isif <= 2 : # fixed cell
            pass
        elif 3 <= isif <= 7 : # variable cell
            anim_vec6d = get_rlx_traj(fname)
    elif 5 <= ibrion <= 8:
        anim_vec6d = get_vib(fname)
    else:
        sys.exit('No IBRION match, auto_creep stop running.')

def get_bornchg(fname='vasprun.xml'):
    xmltree = etr.parse(fname)
    elem_bornchg_set_list = xmltree.xpath('//calculation/array[@name="born_charges"]/set')
    for vset in elem_bornchg_set_list:
        for v in vset:
            print(v.text)

