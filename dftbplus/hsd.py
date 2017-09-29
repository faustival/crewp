
from crewp.dftbplus import type_key, key_type, special_blocks, Write_HSD, Read_HSD

'''
Deal with dictionary containing HSD input key-values of DFTB+
'''

class HSD:

    def __init__(self, fname=None):
        if fname:
            self.read_hsdf(fname)
        else:
            self.nestkeys = {}

    def read_hsdf(self, fname='dftb_in.hsd'):
        hsdf = Read_HSD(fname)
        self.nestkeys = hsdf.get_nestkeys()

    def write_hsdf(self, fname='dftb_inp.hsd'):
        Write_HSD(self.nestkeys, fname)

    def pdos_atoms(self, idx_list, n_rslv=True, l_rslv=True):
        '''
        Generate 'ProjectStates' dictionary
        for PDOS on each atom, index of atom in ``idx_list``
        should match in geometric specification.
        '''
        pdos_keydict = {}
        for idx in idx_list:
            pdos_keydict['dos_atom_'+str(idx)] = {
                    'Atoms' : str(idx),
                    'ShellResolved' : n_rslv,
                    'OrbitalResolved' : l_rslv,
                    }
        if 'Analysis' not in self.nestkeys:
            self.nestkeys['Analysis'] = {}
        self.nestkeys['Analysis']['ProjectStates'] = pdos_keydict

    def get_nestkeys(self,):
        return self.nestkeys


