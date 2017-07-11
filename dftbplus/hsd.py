
import re
import sys
import builtins
from crewp.io.array import read_2darry, wrt_2darry

'''
Reading and writing HSD input file of DFTB+
Keywords are restricted to CamelCase as written in official manual
'''

type_keywords = { 
             'float' : { 
                         'SCCTolerance',
                         'Temperature',
                        },
             'int': {
                         'ParserVersion',
                        },
             'str': { 
                         'Prefix', 
                         'Separator', 
                         'Suffix', 
                         'Atoms',
                         'Label',
                        },
             'bool': {
                         'SCC',
                         'ShellResolved',
                        },
            }

# build inverse relation
keywords_type = {value: key for key, values in type_keywords.items() for value in values}

def autoconv(valstr, key, keywords_type):
    if 'yes' in valstr.lower(): # expect key to be boolean
        val = True
    elif 'no' in valstr.lower():
        val = False
    else: # expect type conversion
        typeconvfunc = keywords_type[key]
        val = getattr(builtins, typeconvfunc)(valstr)
    return val

def get_key_val(line, keywords_type):
    l_str, r_str = [ s.strip() for s in line.split('=') ]
    valstr = r_str.split()[0]
    if '[' in l_str: # expect key have units
        unit = line[ line.index('[')+1 : line.index(']') ].strip()
        key = line[ : line.index('[') ].strip()
        val = autoconv( valstr, key, keywords_type )
        return key, unit, val
    else:
        key = l_str
        val = autoconv( valstr, key, keywords_type )
        return key, val

special_blocks = [ # keywords with content not suitable for recursive dictionary parsing  
        'Geometry', # Gen form or read isolated file
        'MaxAngularMomentum', # Keys are atomic symbols, value could be complicated
        'ProjectStates',  # Repeated 'Region' key
        'KPointsAndWeights', # lines of arrays
        ]

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
        while True:
            line = self.hsdf.readline()
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
                self.nest_keys() 
            elif not line: # Meet EOF
                self.logf.write('# MEET EOF\n')
                break
            elif ('=' in line) and ('{' not in line): # Normal key[unit]-value
                self.logf.write(line[:-1]+'    # Normal KEY-VALUE\n')
                sep = get_key_val(line, keywords_type)
                if len(sep)==3: # expect key have units
                    key, unit, val = sep
                    self.curr_dict[key] = (unit, val)
                elif len(sep)==2:
                    key, val = sep
                    self.curr_dict[key] = val
            elif '}' in line: # dict depth backward, break current recursion
                self.logf.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                break
            elif line.strip()=='': # Blank line, don't put this before EOF
                self.logf.write('    # BLANK LINE\n')
                pass
            else: # meet unmatched pattern, please add new 'elif'.
                self.logf.write(line[:-1]+'    # NOT ASSIGNED CONDITION!!\n')
                break

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
        while True: # find 'Region' block
            line = self.hsdf.readline()
            if 'Region' in line:
                linelist = []
                while True:
                    line = self.hsdf.readline()
                    if '}' in line: # label escape a 'Region' block
                        break
                    elif '=' in line: # find 'Label' to build dictionary
                        if 'Label' in line:
                            _, val = get_key_val(line, keywords_type)
                            region_dict = self.curr_dict[val] = {}
                        else:
                            linelist.append(line)
                for line in linelist: # fill in Region dictionary
                    key, val = get_key_val(line, keywords_type)
                    region_dict[key] = val
            elif '}' in line: # dict depth backward
                self.logf.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                break

    def get_keydict(self):
        self.nest_keys()
        self.logf.close()
        return self.nestkeys

class Write_HSD:

    def __init__(self, nestkeys, hsdf, ):
        self.hsdf = hsdf
        self.nestkeys = nestkeys
        self.write_hsd(self.nestkeys, 0)

    def write_hsd(self, nestdict, ndepth):
        for key, value in nestdict.items():
            if isinstance(value, dict): # depth forward
                if 'key_attr' in value:
                    self.hsdf.write('  '*ndepth+key+' = '+value['key_attr']+' {\n')
                else:
                    self.hsdf.write('  '*ndepth+key+' = '+' {\n')
                if key in special_blocks:
                    self.curr_dict = value
                    getattr(self, 'write_'+key.lower())(ndepth+1)
                else:
                    self.write_hsd(value, ndepth+1)
                self.hsdf.write('  '*ndepth+'}\n')
            elif key !='key_attr': # normal key-value
                self.hsdf.write('  '*ndepth + key + ' = ' + str(value) + '\n')

    def write_geometry(self, ndepth):
        if 'key_attr' in self.curr_dict and \
        self.curr_dict['key_attr']=='GenFormat':
            self.hsdf.write('  '*ndepth + '<<< ' + self.curr_dict['genfname'] + '\n')

    def write_maxangularmomentum(self, ndepth):
        pass

    def write_kpointsandweights(self, ndepth):
        pass

    def write_projectstates(self, ndepth):
        pass

