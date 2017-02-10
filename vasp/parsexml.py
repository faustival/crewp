#! /usr/bin/python3

import lxml.etree as etr
import numpy as np
from crewp.lattice.coordtrans import frac2cart
import sys

'''
# delete these typing function after test 
'''
def type_varray(arrayname, ary2):
    '''
    Printing 2-index array, i.e., matrix
    '''
    print("  Printing 2d-array: ", arrayname, )
    for vec in ary2:
        print( '   '+' '.join( '{:13.8f}'.format(entry) for entry in vec ) )
    print('\n')

def type_step_varrays(arrayname, ary3):
    print("Printing arrays: ", arrayname, )
    for i, ary2 in enumerate(ary3):
        ary2dname = 'STEP: '+'{:d}'.format(i)
        type_varray(ary2dname, ary2)

'''
latvec_init: initial lattice cell vectors, 
            shape( 3, 3)
vib_eigvec: vibrational eigenvectors of Hessian
            shape( nDOF, nDOF), DOF: Degree of freedom
            for systems with frozen coordinates, (nDOF != 3*natoms)
===================================================================
position_steps: atomic positions of each SCF step in fractional crystal coordinate, 
            shape( nsteps, natoms, 3)
latvec_steps: lattice cell vectors in each SCF step, 
            shape( nsteps, 3, 3)
force_steps: forces of each SCF step,
            shape( nsteps, natoms, 3)
'''
xpath_dict = { 
        'latvec_init' : '//structure[@name="initialpos"]/crystal/varray[@name="basis"]' , # expected single
        'vib_eigvec' : '//calculation/dynmat/varray[@name="eigenvectors"]' , # expected single
        'position_steps' : '//calculation/structure/varray[@name="positions"]' , # expected steps 
        'latvec_steps' : '//calculation/structure/crystal/varray[@name="basis"]' , # expected steps
        'force_steps' : '//calculation/varray[@name="forces"]' , # expected steps
        }

class ParseXML:

    def __init__(self, fname='vasprun.xml', ):
        self.xmltree = etr.parse(fname)

    def varray2darry(self, elem_varray):
        '''
        Arrange data in ``elem_varray`` element (e.g., <varray>)
        into numpy 2d-array.
        '''
        varray = [] # len = nvectors
        for elem_vec in elem_varray:
            varray.append( [ float(a) for a in elem_vec.text.split() ] )
        return np.array(varray)

    def get_varray(self, xpathcode, ):
        '''
        Only for varray matching ``xpathcode`` ONCE
        '''
        elem_varray = self.xmltree.xpath(xpathcode) # note to unpack 
        if len(elem_varray) != 1:
            sys.exit('From get_varray, xpathcode returns not ONLY ONE match!')
        elem_varray, = elem_varray
        varray = self.varray2darry(elem_varray)
        return varray

    def get_varray_steps(self, xpathcode, ):
        '''
        Stack 2D-arrays in each SCF step, 
        from parsing 2D-arrays in <varray> tag, 
        returns :
        varray_steps: shape( nsteps, nvectors, vector_dim)
        '''
        elem_list = self.xmltree.xpath(xpathcode)
        varray_steps = [] # len = number of steps
        for elem_varray in elem_list :
            varray = self.varray2darry(elem_varray)
            varray_steps.append(varray)
        return np.array(varray_steps)

    def auto_creep(self, ):
        '''
        # Get required parameters for auto creep:
        #   IBRION, ISIF
        '''
        elem_ibrion, = self.xmltree.xpath('//parameters/separator[@name="ionic"]/i[@name="IBRION"]') # don't parse <incar> tag
        elem_isif, = self.xmltree.xpath('//parameters/separator[@name="ionic"]/i[@name="ISIF"]') # don't parse <incar> tag
        ibrion = int(elem_ibrion.text)
        isif = int(elem_isif.text)
        if -1 <= ibrion <= 3: # ionic steps
            position_steps = self.get_varray_steps(xpath_dict['position_steps'],) # fractional coordinate
            force_steps = self.get_varray_steps(xpath_dict['force_steps'],)
            if 0 <= isif <= 2 : # fixed cell
                latvec_init = self.get_varray(xpath_dict['latvec_init'],)
                position_steps_cart = []
                for i in range(len(position_steps)):
                    position_steps_cart.append( frac2cart( position_steps[i], latvec_init ) )
            elif 3 <= isif <= 7 : # variable cell
                latvec_steps = self.get_varray_steps(xpath_dict['latvec_steps'],)
                position_steps_cart = []
                for i in range(len(position_steps)):
                    position_steps_cart.append( frac2cart( position_steps[i], latvec_steps[i] ) )
            type_step_varrays('position_steps_cart', position_steps_cart) # print to check arrays
        elif 5 <= ibrion <= 8: # vibrational frequencies
            pass
        else:
            sys.exit('No IBRION match, auto_creep stop running.')

    def get_bornchg(self, ):
        elem_bornchg_set_list = self.xmltree.xpath('//calculation/array[@name="born_charges"]/set')
        for vset in elem_bornchg_set_list:
            for v in vset:
                print(v.text)

