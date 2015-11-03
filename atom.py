#! /usr/bin/python3

class Atom:
    '''
    self.atomid : atom ID in output, integer
    self.elem : element of atom, string
    '''
    def __init__(self, atomid, elem):
        self.atomid = atomid
        self.elem = elem

    def get_ldos(self, oupfpre, orbitals, readpdos=True, spin=False):
        '''
        Read the pdos files of the atom.

        pdos file structure:
        ====================
        <beginning of file>
        # E (eV)  ldosup(E)  ldosdw(E) pdosup(E)  pdosdw(E)  ...
         -6.759  0.944E-07  0.942E-07  0.944E-07  0.942E-07  ...
         ...
         ...
        <end of file>

        pdos : projected on each atomic orbitals, e.g., p_x, p_y, p_z
        ldos : sum of pdos

        INPUT:
        ======
        oupfpre : prefix of pdos files, indicated by QE input ``filpdos`` of projwfc.x 
        readpdos : if True, read pdos and ldos
                   if False, read only ldos
        orbitals : list of projection orbitals

        NEW Attributes:
        ===============
        '''
        # dictionary building correspondence of orbital ID
        orbital_dict = { 's':'1', 'p':'2', 'd':'3', 'f':'4' }
        for orbital in orbitals:
            pdosfname = oupfpre + \
                        '.pdos_atm#' + str(self.atomid) + \
                        '(' + self.elem + ')_wfc#' + \
                        orbital_dict[orbital] + '(' + orbital + ')'
            print(pdosfname)





