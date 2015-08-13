#! /usr/bin/python3

import numpy as np
from plotio_read import PlotIORead
from chrg_avgz import ChrgAvgZ
from slab_indchrg import SlabIndChrg


class SlabFreeChrg:
    '''
    use the class 
        PlotIORead : Read 3d-charge data and system info from 
                     PW output file
        ChrgAvgZ   : Compute the xy-plane averaged charge

    Sequence of charge density list:
    [total, d, free]
    '''

    def __init__(self, slabdict):
        '''
        Example input `slabdict` structure:
        { 'elem':'Au', 'ort':'111', 'bands':[60,35] }
        '''
        self.elem  = slabdict['elem']
        self.ort   = slabdict['ort']
        self.bands = slabdict['bands']
        # get info from 0-field charge output
        inpf = self.inpfname(self.bands[0], 0.0)
        slabinit = PlotIORead(inpf)
        slabinfo = ChrgAvgZ(slabinit.ary3d, slabinit.cell)
        self.zaxis = slabinfo.zgrid()
        # get 0-field averaged z-charge densities
        self.chrgz_nofld = self.chrgz(0.0)

    def inpfname(self, nband, field):
        inpfname = self.elem.lower() + \
                   self.ort + \
                   'f%3.3d' %int(field*100.) + \
                   '_ncpp/' + \
                   'chrgsum_' + \
                   '%3.3d' %nband
        return inpfname

    def avgchrg(self, inpfname):
        '''
        Read charge from PW output file, compute the average z-charge
        The most cost routine in the Class
        '''
        chrgdata = PlotIORead(inpfname, 'ang')
        slabchrg = ChrgAvgZ(chrgdata.ary3d, chrgdata.cell)
        avgchrg = slabchrg.xyavg()#*slabchrg.xyarea()
        return avgchrg

    def chrgz(self, field):
        '''
        Get free averaged charge
        '''
        inpf_tot = self.inpfname(self.bands[0], field)
        inpf_d   = self.inpfname(self.bands[1], field)
        # read and compute for total, d, free z-charge
        chrgz_tot  = self.avgchrg(inpf_tot)
        chrgz_d    = self.avgchrg(inpf_d)
        chrgz_free = chrgz_tot - chrgz_d
        return [chrgz_tot, chrgz_d, chrgz_free]

    def flddiff(self, field):
        '''
        Get difference z-charge of field
        '''
        # 
        chrgz_fld = self.chrgz(field)
        chrgdiff = [ (chrgz_fld[i] - self.chrgz_nofld[i]) for i in range(0,3) ]
        return chrgdiff

    def get_flddiff(self):
        '''
        note temporary only 0.1 field was required
        change `field` to data-structure if need
        '''
        self.chrgz_fld = self.flddiff(0.1)





