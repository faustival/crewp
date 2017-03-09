
from crewp.vasp.chgcar import read_chg
from crewp.qe.plotio_read import plotio_read

from crewp.chrg_avgz import ChrgAvgZ

def get_chrg_avgz(fname, packname):
    if packname == 'vasp': 
        chrgden, cell = read_chg(fname)
    if packname == 'qe': 
        chrgden, cell, _, = plotio_read(fname)
    chrg_obj = ChrgAvgZ(chrgden, cell)
    chrg_z = chrg_obj.xyavg()
    z_ax = chrg_obj.zgrid()
    return chrg_z, z_ax

