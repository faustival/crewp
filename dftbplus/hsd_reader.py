
'''
Read HSD input file of DFTB+
    Data stored in nested dictionary Read_HSD.nestkeys
'''

import sys
import builtins
from crewp.io.array import read_2darry
from crewp.dftbplus import type_key, key_type, special_blocks

def get_key_val(line, key_type):
    '''
    Auto split line like:
        'key [unit] = val'
    return if unit in line
    '''
    l_str, r_str = [ s.strip() for s in line.split('=') ]
    valstr = r_str.split()[0]
    if '[' in l_str: # expect key have units
        unit = line[ line.index('[')+1 : line.index(']') ].strip()
        key = line[ : line.index('[') ].strip()
        val = autoconv( valstr, key, key_type )
        return key, unit, val
    else:
        key = l_str
        val = autoconv( valstr, key, key_type )
        return key, val

def autoconv(valstr, key, key_type):
    '''
    Type conversion depend on ``key_type`` dictionary
    '''
    if 'yes' in valstr.lower(): # expect key to be boolean
        val = True
    elif 'no' in valstr.lower():
        val = False
    else: # expect type conversion
        typeconvfunc = key_type[key]
        val = getattr(builtins, typeconvfunc)(valstr)
    return val

def dict_from_path(keypath, dictroot): 
    '''
    Auxiliary function locate to a depth of nested dictionary
    with path indicated by keypath list.
    '''
    d = dictroot
    for key in keypath:
        d = d[key]
    return d

class Read_HSD: 

    def __init__(self, fname = 'dftb_in.hsd'):
        self.hsdf = open(fname, 'r')
        self.logf = open('read_hsd.log', 'w')
        self.keypath = []
        self.nestkeys = {}
        self.curr_dict = self.nestkeys

    def nest_keys(self): # recursive build nested-key
        line = self.hsdf.readline()
        if not line: # Meet EOF
            self.logf.write('# MEET EOF\n')
        else:
            if '{' in line: # dict depth forward
                self.logf.write(line[:-1]+ '    # DEPTH FORWARD\n')
                try: # key has attribute
                    key = line[0:line.index('=')].strip()
                    key_attr = line[ line.index('=')+1 : line.index('{') ].strip()
                except ValueError: # key without attribute
                    key = line[0:line.index('{')].strip()
                    key_attr = ''
                self.curr_dict = dict_from_path(self.keypath, self.nestkeys) 
                self.curr_dict[key] = {} # initialize new key:dictionary
                self.keypath.append(key)
                self.curr_dict = self.curr_dict[key] # forward 1 depth
                if key_attr: 
                    self.curr_dict['key_attr'] = key_attr
                if key in special_blocks: # call function read special blocks
                    getattr(self, 'read_'+key.lower())()
                    self.curr_dict = dict_from_path(self.keypath, self.nestkeys) 
            elif '}' in line: # dict depth backward, break current recursion
                self.logf.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                self.curr_dict = dict_from_path(self.keypath, self.nestkeys) 
            elif ('=' in line) and ('{' not in line): # Normal key[unit]-value
                self.logf.write(line[:-1]+'    # Normal KEY-VALUE\n')
                sep = get_key_val(line, key_type)
                if len(sep)==3: # expect key have units
                    key, unit, val = sep
                    self.curr_dict[key] = (unit, val)
                elif len(sep)==2:
                    key, val = sep
                    self.curr_dict[key] = val
            elif line.strip()=='': # Blank line, don't put this before EOF
                self.logf.write('    # BLANK LINE\n')
                pass
            else: # meet unmatched pattern, please add new 'elif'.
                sys.exit('Class Read_HSD: '+line[:-1]+'    # NOT ASSIGNED CONDITION!!\n')
            self.nest_keys()

    def read_geometry(self):
        if 'key_attr' in self.curr_dict and \
        self.curr_dict['key_attr']=='GenFormat':
            while True:
                line = self.hsdf.readline()
                if '<<<' in line:
                    genfname = line.strip().strip('<').strip().strip('"')
                    self.curr_dict['genfname'] = genfname
                elif '}' in line: # dict depth backward
                    self.logf.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                    del self.keypath[-1] # backward 1 depth
                    break

    def read_maxangularmomentum(self):
        while True:
            line = self.hsdf.readline()
            if '=' in line:
                key, val = [ s.strip() for s in line.split('=') ]
                self.curr_dict[key] = val
            elif '}' in line: # dict depth backward
                self.logf.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                break

    def read_kpointsandweights(self):
        if self.curr_dict['key_attr'] == 'SupercellFolding':
            self.curr_dict['kmesh'] = read_2darry( self.hsdf, 3, 'int')
            self.curr_dict['kshift'], = read_2darry( self.hsdf, 1, 'float')
        while True:
            line = self.hsdf.readline()
            if '}' in line: # dict depth backward
                self.logf.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                break

    def read_projectstates(self):
        '''
        ProjectStates: { 
            'region_i'  : {
                              'Atoms' : '***',
                              'ShellResolved' : True,
                              'Label' : '***',
                              ...
                          },
            ...
                       }
        '''
        i_region = 0
        while True: # find 'Region' block
            '''
            Build ``region_dict`` with key 'region_i'
            Stack other line strings, fill in the ``region_dict`` 
            '''
            line = self.hsdf.readline()
            if 'Region' in line:
                i_region += 1
                region_dict = self.curr_dict['region_'+str(i_region)] = {}
                while True: 
                    line = self.hsdf.readline()
                    if '}' in line: # label escape a 'Region' block
                        break
                    elif '=' in line: 
                        key, val = get_key_val(line, key_type)
                        region_dict[key] = val
            elif '}' in line: # dict depth backward
                self.logf.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                break

    def get_nestkeys(self):
        self.nest_keys()
        self.logf.close()
        return self.nestkeys

