
'''
Write HSD input file of DFTB+
    Data from nested dictionary nestkeys
'''

import numpy as np
import sys
from crewp.io.array import wrt_2darry
from crewp.dftbplus import type_key, key_type, special_blocks

def auto_str(val, ):
    '''
    Automatically determine the type of ``val`` 
    and transform to str type
    '''
    if type(val)==bool: 
        if val: valstr = 'Yes'
        else: valstr = 'No'
    elif type(val)==int: 
        valstr = '{:d}'.format(val)
    elif type(val)==float:
        valstr = '{:13.8e}'.format(val)
    elif type(val)==str:
        valstr = val.strip()
    else:
        sys.exit('Function: auto_str: '+ str(val) + ', type not defined !!\n')
    return valstr

class Write_HSD:

    def __init__(self, nestkeys, fname='dftb_in.hsd', ):
        self.hsdf = open(fname, 'w')
        self.nestkeys = nestkeys
        self.write_hsd(self.nestkeys, 0)
        self.hsdf.close()

    def write_key_val(self, ndepth, key, val, ):
        '''
        write single line pattern: key [unit] = val
        '''
        self.hsdf.write('  '*ndepth + key)
        if isinstance(val, tuple): # key has [unit]
            self.hsdf.write(' ['+ str(val[0]) + '] = ' + auto_str(val[1]) )
        else:
            self.hsdf.write( ' = ' + auto_str(val) )
        self.hsdf.write('\n')

    def write_hsd(self, nestdict, ndepth):
        for key, val in nestdict.items():
            if isinstance(val, dict): # depth forward
                if 'key_attr' in val:
                    self.hsdf.write('  '*ndepth+key+' = '+val['key_attr']+' {\n')
                else:
                    self.hsdf.write('  '*ndepth+key+' = '+' {\n')
                if key in special_blocks:
                    self.curr_dict = val
                    getattr(self, 'write_'+key.lower())(ndepth+1)
                else:
                    self.write_hsd(val, ndepth+1)
                self.hsdf.write('  '*ndepth+'}\n')
                if ndepth==0:
                    self.hsdf.write('\n')
            elif key !='key_attr': # normal key-val
                self.write_key_val(ndepth, key, val)

    def write_geometry(self, ndepth):
        if 'key_attr' in self.curr_dict and \
        self.curr_dict['key_attr']=='GenFormat':
            self.hsdf.write('  '*ndepth + '<<< ' + self.curr_dict['genfname'] + '\n')

    def write_maxangularmomentum(self, ndepth):
        for key, val in self.curr_dict.items():
            self.hsdf.write('  '*ndepth + key + ' = ' + val + '\n')

    def write_kpointsandweights(self, ndepth):
        if self.curr_dict['key_attr'] == 'SupercellFolding':
            wrt_2darry( self.curr_dict['kmesh'], title='', rowtags='  '*ndepth, wtype='int', f=self.hsdf, )
            wrt_2darry( np.array( [ self.curr_dict['kshift'] ] ), title='', rowtags='  '*ndepth, f=self.hsdf )

    def write_projectstates(self, ndepth):
        for key, val in self.curr_dict.items():
            self.hsdf.write('  '*ndepth + 'Region {\n')
            if 'Label' not in val:
                self.write_key_val(ndepth+1, 'Label', key)
            for key1, val1 in self.curr_dict[key].items():
                self.write_key_val(ndepth+1, key1, val1)
            self.hsdf.write('  '*ndepth + '}\n')

