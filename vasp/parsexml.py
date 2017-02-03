#! /usr/bin/python3

import lxml.etree as etr
import numpy as np
from crewp.lattice.coordtrans import frac2cart

def type_step_arrays(arrayname, ary3):
    '''
    # delete this checking function after test 
    '''
    print("Printing array: ", arrayname, )
    for i, coordstep in enumerate(ary3):
        print("STEP ", i)
        for coord in coordstep:
            print( '   '+' '.join( '{:13.8f}'.format(entry) for entry in coord ) )
        print('\n')

def get_latvec(fname='vasprun.xml'):
    pass

def get_rlx_steps_latvec(fname='vasprun.xml'):
    '''
    latvec_steps: lattice cell vectors in each SCF step, 
    shape( nsteps, 3, 3)
    '''
    xmltree = etr.parse(fname)
    elem_latvec_list = xmltree.xpath('//calculation/structure/crystal/varray[@name="basis"]')
    latvec_steps = [] # len = number of steps
    for elem_latvec in elem_latvec_list :
        latvec = [] # len = 3        
        for elem in elem_latvec:
            latvec.append( [ float(a) for a in elem.text.split() ] )
        latvec_steps.append(latvec)
    return np.array(latvec_steps)

def get_rlx_steps_pos(fname='vasprun.xml'):
    '''
    pos_steps: atomic positions of each SCF step in fractional crystal coordinate, 
    shape( nsteps, natoms, 3)
    '''
    xmltree = etr.parse(fname)
    elem_position_list = xmltree.xpath('//calculation/structure/varray[@name="positions"]')
    pos_steps = [] # len = number of steps
    for elem_position in elem_position_list:
        pos = [] # len = number of atoms
        for elem in elem_position:
            pos.append( [ float(a) for a in elem.text.split() ] )
        pos_steps.append(pos)
    return np.array(pos_steps)

def get_rlx_steps_forc(fname='vasprun.xml'):
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
    if 1 <= ibrion <= 3: # ionic relax
        if 0 <= isif <= 2 : # fixed cell
            pos3 = get_rlx_steps_pos(fname)
        elif 3 <= isif <= 7 : # variable cell
            pos_steps = get_rlx_steps_pos(fname)
            latvec_steps = get_rlx_steps_latvec(fname)
            pos_steps_cart = []
            for i in range(len(pos_steps)):
                pos_steps_cart.append( frac2cart( pos_steps[i], latvec_steps[i] ) )
            type_step_arrays('pos_steps_cart', pos_steps_cart) # print to check arrays
    elif 5 <= ibrion <= 8: # vibrational frequencies
        anim_vec6d = get_vib(fname)
    else:
        sys.exit('No IBRION match, auto_creep stop running.')

def get_bornchg(fname='vasprun.xml'):
    xmltree = etr.parse(fname)
    elem_bornchg_set_list = xmltree.xpath('//calculation/array[@name="born_charges"]/set')
    for vset in elem_bornchg_set_list:
        for v in vset:
            print(v.text)

