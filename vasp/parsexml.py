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

        '''
        pos_steps: atomic positions of each SCF step in fractional crystal coordinate, 
                   shape( nsteps, natoms, 3)
        latvec_steps: lattice cell vectors in each SCF step, 
                   shape( nsteps, 3, 3)
        '''
xpath_dict = { 
        'pos_steps' : '//calculation/structure/varray[@name="positions"]' ,  
        'latvec_steps' : '//calculation/structure/crystal/varray[@name="basis"]' ,
        }

def get_varray_steps(xpathcode, fname='vasprun.xml', ):
    '''
    parsing 2D-arrays in <varray> tag, 
    arrays in each SCF step is stacked
    varray_steps: shape( nsteps, nvectors, vector_dim)
    '''
    xmltree = etr.parse(fname)
    elem_list = xmltree.xpath(xpathcode)
    varray_steps = [] # len = number of steps
    for elem_varray in elem_list :
        varray = [] # len = nvectors
        for elem in elem_varray:
            varray.append( [ float(a) for a in elem.text.split() ] )
        varray_steps.append(varray)
    return np.array(varray_steps)

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
            pos_steps = get_varray_steps(xpath_dict['pos_steps'], fname)
        elif 3 <= isif <= 7 : # variable cell
            pos_steps = get_varray_steps(xpath_dict['pos_steps'], fname)
            latvec_steps = get_varray_steps(xpath_dict['latvec_steps'], fname)
            pos_steps_cart = []
            for i in range(len(pos_steps)):
                pos_steps_cart.append( frac2cart( pos_steps[i], latvec_steps[i] ) )
            type_step_arrays('pos_steps_cart', pos_steps_cart) # print to check arrays
    elif 5 <= ibrion <= 8: # vibrational frequencies
        pass
    else:
        sys.exit('No IBRION match, auto_creep stop running.')

def get_bornchg(fname='vasprun.xml'):
    xmltree = etr.parse(fname)
    elem_bornchg_set_list = xmltree.xpath('//calculation/array[@name="born_charges"]/set')
    for vset in elem_bornchg_set_list:
        for v in vset:
            print(v.text)

