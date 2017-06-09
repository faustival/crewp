
import sys
import os
import numpy as np
import lxml.etree as etr
from crewp.lattice.lattice import frac2cart

'''
latvec_init: initial lattice cell vectors, 
            shape( 3, 3)
selectdyn_init: boolean array of initial selective dynamics 
            shape( natoms, 3)
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
        'position_init' : '//structure[@name="initialpos"]/varray[@name="positions"]' , # expected single
        'selectdyn_init' : '//structure[@name="initialpos"]/varray[@name="selective"]' , # expected single
        'vib_eigvec' : '//calculation/dynmat/varray[@name="eigenvectors"]' , # expected single
        'position_steps' : '//calculation/structure/varray[@name="positions"]' , # expected steps 
        'latvec_steps' : '//calculation/structure/crystal/varray[@name="basis"]' , # expected steps
        'force_steps' : '//calculation/varray[@name="forces"]' , # expected steps
        }

class ParseXML:

    def __init__(self, fname='vasprun.xml', ):
        if not os.path.isfile(fname):
            sys.exit('From crewp.vasp.parsexml.ParseXML, ' \
                      +'file does not exist: '+fname)
        self.xmltree = etr.parse(fname)

    def varray2darry(self, elem_varray, vtype='float',):
        '''
        Arrange data in ``elem_varray`` element (e.g., <varray>)
        into numpy 2d-array.
        '''
        varray = [] # len = nvectors
        if vtype=='float':
            for elem_vec in elem_varray:
                varray.append( [ float(a) for a in elem_vec.text.split() ] )
        elif vtype=='boolean':
            for elem_vec in elem_varray:
                varray.append( [ a=='T' for a in elem_vec.text.split() ] )
        return np.array(varray)

    def get_varray(self, xpathcode, ):
        '''
        Only for varray matching ``xpathcode`` ONCE
        '''
        elem_varray = self.xmltree.xpath(xpathcode) # note to unpack 
        if len(elem_varray) != 1:
            sys.exit('From get_varray, xpathcode returns not ONLY ONE match!')
        elem_varray, = elem_varray
        if ('type' in elem_varray.attrib) and (elem_varray.attrib['type']=="logical"): # boolean array
            varray = self.varray2darry(elem_varray, 'boolean')
        else: # float array
            varray = self.varray2darry(elem_varray)
        return varray

    def get_3dvarray(self, xpathcode, ):
        '''
        Stack 2D-arrays in each xpathcode match into 3d-arrays, 
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

    def get_atomlist(self, ):
        elem_atomlist = self.xmltree.xpath('//atominfo/array[@name="atoms"]/set/rc/c[1]')
        atomlist = [ elem.text for elem in elem_atomlist]
        return atomlist

    def get_vibeig_coord(self, ):
        '''
        Fill the full eigenvector of vibrational dynamical matrix 
            (DOF frozen was filled zero), and reshape as 3Darray
            to adapt natom*3 coordinate-type arrays.
        vibeig_coord: shape( ndof, natoms, 3 )
        '''
        eigarry = self.get_varray(xpath_dict['vib_eigvec'],)
        selectdynarry = self.get_varray(xpath_dict['selectdyn_init'],) # boolean
        natoms = selectdynarry.shape[0] # number of atoms
        ndof = eigarry.shape[0] # number of degree of freedoms
        selectdynarry1d = np.reshape(selectdynarry, (3*natoms), )
        eigaugarry = np.zeros((3*natoms, ndof))
        eigaugarry[ selectdynarry1d ] = np.transpose(eigarry, ) # fill by boolean  
        eigaugarry = np.transpose(eigaugarry, )
        vibeig_coord = np.reshape(eigaugarry, (ndof, natoms, 3), )
        return vibeig_coord 

    def auto_creep(self, ):
        '''
        # Get required parameters for auto creep:
        #   IBRION, ISIF attached to self
        '''
        elem_ibrion, = self.xmltree.xpath('//parameters/separator[@name="ionic"]/i[@name="IBRION"]') # don't parse <incar> tag
        elem_isif, = self.xmltree.xpath('//parameters/separator[@name="ionic"]/i[@name="ISIF"]') # don't parse <incar> tag
        ibrion = int(elem_ibrion.text)
        isif = int(elem_isif.text)
        self.ibrion = ibrion
        self.isif = isif
        if -1 <= ibrion <= 3: # ionic steps
            position_steps_frac = self.get_3dvarray(xpath_dict['position_steps'],) # fractional coordinate
            force_steps = self.get_3dvarray(xpath_dict['force_steps'],)
            selectdynarry = self.get_varray(xpath_dict['selectdyn_init'],) # boolean
            force_steps[:, selectdynarry==False ] = 0. # mask constraint for forces
            if 0 <= isif <= 2 : # fixed cell
                latvec = self.get_varray(xpath_dict['latvec_init'],) # 2d-array
                position_steps = []
                for i in range(len(position_steps_frac)):
                    position_steps.append( frac2cart( position_steps_frac[i], latvec ) )
            elif 3 <= isif <= 7 : # variable cell
                latvec = self.get_3dvarray(xpath_dict['latvec_steps'],) # steps as 3d-array
                position_steps = []
                for i in range(len(position_steps_frac)):
                    position_steps.append( frac2cart( position_steps_frac[i], latvec[i] ) )
            '''
            pass return values
            '''
            latvec = latvec
            position = position_steps
            anim_vecs = force_steps
        elif 5 <= ibrion <= 8: # vibrational frequencies
            latvec = self.get_varray(xpath_dict['latvec_init'],) # 2d-array
            position_frac = self.get_varray(xpath_dict['position_init'],) # 2d-array
            position = frac2cart( position_frac, latvec )
            vibeig_coord = self.get_vibeig_coord()
            '''
            pass return values
            '''
            latvec = latvec
            position = position
            anim_vecs = vibeig_coord
        else:
            sys.exit('No IBRION match, auto_creep stop running.')
        return latvec, position, anim_vecs

