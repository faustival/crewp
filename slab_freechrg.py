#! /usr/bin/python3

import numpy as np
from scipy.integrate import simps
from .qe.plotio_read import PlotIORead
from chrg_avgz import ChrgAvgZ


class SlabFreeChrg:
    '''
    use the class 
        PlotIORead : Read 3d-charge data and system info from 
                     PW output file
        ChrgAvgZ   : Compute the xy-plane averaged charge

    Sequence of field-dependent z-charge density list:
    self.chrgz = [
                  [total, d, free], # 0.0 field
                  [total, d, free], # 1st field
                  ...
                 ]

    self.freeratio = [ 0.0_field, 1st_field, ... ]
        
    self.chrgz_diffld = [
                  [total, d, free], # 1st field
                  ...
                 ]
    '''

    def __init__(self, slabdict):
        '''
        Example input `slabdict` structure:
        { 'elem':'Au', 'ort':'111', 'bands':[60,35], 'flds':[0.0, 0.1] },
        '''
        self.elem    = slabdict['elem']
        self.ort     = slabdict['ort']
        self.bands   = slabdict['bands']
        self.flds    = slabdict['flds']
        self.shift   = slabdict['shift']
        self.slablmt = slabdict['slablmt']
        # get info from 0-field charge output
        inpf = self.inpfname(self.bands[0], 0.0)
        slabinit = PlotIORead(inpf, 'ang')
        self.cell = slabinit.cell
        slabinfo = ChrgAvgZ(slabinit.ary3d, slabinit.cell)
        atom_coord = slabinit.atom_coord
        self.xyarea = slabinfo.xyarea()
        # z-shift dependent variables
        self.zatom = slabinfo.zatompos(atom_coord)
        self.zaxis = slabinfo.zgrid()
        # get 0-field averaged z-charge densities
        self.chrgz = [self.get_chrgz(0.0)]

    def zshift_layer(self):
        '''
        shift coordinate reference along z-axis
        self.shift to indicate the n-th max top atom
        '''
        zshft = self.zatom[self.shift]
        self.zaxis -= zshft
        self.zatom -= zshft
        if hasattr(self, 'imgplane'):
            self.imgplane = [ (imgplane - zshft) for imgplane in self.imgplane ]

    def inpfname(self, nband, field):
        inpfname = self.elem.lower() + \
                   self.ort + \
                   'f%5.5d' %int(field*10000.) + \
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

    def get_chrgz(self, field):
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

    def get_imgplane(self, chrgind):
        # extract proper integrate region
        idx_center = np.argmin(np.absolute(self.zaxis-self.slabcenter))
        chrgind_var = chrgind[idx_center:]
        zaxis_var = self.zaxis[idx_center:]
        # calculate the image plane position
        int_zrho = simps(chrgind_var*zaxis_var, zaxis_var)
        int_rho = simps(chrgind_var, zaxis_var)
        z0 = int_zrho/int_rho
        return z0
    
    def get_bulkfreeden(self):
        '''
        compute bulk free charge density with total charge
        NOTE only useful if system has no vacuum layer, i.e. bulk
        '''
        self.int_freechrg = simps(self.chrgz[0][2], self.zaxis)*self.xyarea
        self.cellvol = self.xyarea*self.cell[2,2]
        self.bulkfreeden = self.int_freechrg/self.cellvol

    def set_chrgz_fld(self):
        '''
        append z-charge data of all field 
        '''
        for field in self.flds[1:]:
            chrgz_fld = self.get_chrgz(field)
            self.chrgz.append(chrgz_fld)

    def set_flddiff(self):
        '''
        change `field` to data-structure if need
        '''
        self.chrgz_diffld = []
        for i in range(1,len(self.flds)):
            chrgz_diffld = [ (self.chrgz[i][j] - self.chrgz[0][j]) for j in range(0,3) ] 
            self.chrgz_diffld.append(chrgz_diffld)

    def set_freeratio(self, bulkden):
        '''
        compute rhoz(free)/bulkden
        '''
        self.freeratio = []
        for [total, d, free] in self.chrgz:
            self.freeratio.append(free/bulkden)

    def set_imgplane(self):
        '''
        self.slablmt: [index_top_atom, index_bottom_atom]
        reference to `self.zatom`
        (Note `self.zatom` is in descending order.)
        '''
        # compute center position of slab
        self.slabcenter = .5*(self.slablmt[0] + self.slablmt[1])
        self.imgplane = []
        for chrgz_diffld in self.chrgz_diffld:
            chrgz_ind = chrgz_diffld[0]
            z0 = self.get_imgplane(chrgz_ind)
            self.imgplane.append(z0)

    def wrtdata(self):
        for i in range(0,len(self.flds)):
            data = tuple( [self.zaxis] + self.chrgz[i] )
            datfname = self.elem.lower() + \
                       self.ort + \
                       'f%5.5d' %int(self.flds[i]*10000.) + \
                       '_ncpp.dat' 
            headtag = ' zaxis    full_valence     d-valence     free-valence  '
            np.savetxt(datfname, np.column_stack(data), header=headtag)

    def wrtratio(self):
        data = tuple( [self.zaxis] + self.freeratio )
        datfname = self.elem.lower() + \
                   self.ort + \
                   'chrgratio' + \
                   '_ncpp.dat' 
        fieldstrlist = ['f_'+str(field) for field in self.flds]
        headtag = ' zaxis '  + '  '.join(fieldstrlist) 
        np.savetxt(datfname, np.column_stack(data), header=headtag)




