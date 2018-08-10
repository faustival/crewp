
import sys
import numpy as np
from ase.io import read as ase_read
from crewp.dftbplus.hsd import HSD
from crewp.io.array import wrt_1darry

orb_chrg_entry = { 
            's': 1,
            'p': 4,
            'd': 9,
           }

def read_chrg(genfname='geoinp.gen', chrg_fname='charges.dat', hsdfname='dftb_in.hsd', ):
    '''
    Prerequisites: 
        * charges.dat to be read;  
        * correspondence ``.gen``  
        * input ``dftb_in.hsd`` 
    Intermediates:
        max_orbital_dict: { 'Au':'d', O:'p', ... }
    '''
    # read chem_symbol:max_orbital from HSD input
    hsd = HSD(hsdfname)
    max_orbital_dict = hsd.get_nestkeys()['Hamiltonian']['MaxAngularMomentum'] 
    # read chem_symbol list from .gen file
    atoms = ase_read(filename=genfname, format='gen')
    chemsymbol_list = atoms.get_chemical_symbols()
    # read charges.dat  
    with open(chrg_fname, 'r') as chrgf:
        # read header and transform strings into proper type 
        headline = chrgf.readline()
        version, t_blockcharges, t_imaginaryblock, nspin, checksum = headline.split()
        version, t_blockcharges, t_imaginaryblock, nspin, checksum = int(version), t_blockcharges=='T', t_imaginaryblock=='T', int(nspin), float(checksum)
        if t_blockcharges or  t_imaginaryblock:
            sys.exit("Reading "+chrg_fname+", not implemented case for current 'tBlockCharges tImaginaryBlock'.")
        chrg_list = []
        for chemsymbol in chemsymbol_list:
            n_chrgentry = orb_chrg_entry[max_orbital_dict[chemsymbol]]
            chrg_str = np.fromfile(chrgf, count=n_chrgentry, sep=' ')
            chrg_list.append( float(chrg_str[0]) )
    chrg_arry = np.array(chrg_list)
    return chrg_arry 

def write_chrg(chrg_arry, chemsymbol_list, max_orbital_dict, chargesfname='charges_from_crewp.dat' ):
    with open(chargesfname, 'w') as f:
        f.write( ' 3 F F 1 '+'{:>.12f}'.format(chrg_arry.sum())+'\n' )
        for i, chrg in enumerate(chrg_arry):
            chemsymbol = chemsymbol_list[i]
            n_chrgentry = orb_chrg_entry[max_orbital_dict[chemsymbol]]
            # charge array for an atom, to be written
            chrg_arry_atom = np.zeros((n_chrgentry)) 
            chrg_arry_atom[0] = chrg
            wrt_1darry(chrg_arry_atom, col_lim=3, f=f, fmt='{:<16.12f}' )
