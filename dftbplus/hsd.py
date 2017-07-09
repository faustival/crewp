
import sys

'''
Reading and writing HSD input file of DFTB+
Keywords are restricted to CamelCase as written in official manual
'''

special_keys = [ # keywords with content not suitable for recursive dictionary parsing  
        #'ProjectStates',  # Repeated 'Region' key
        'KPointsAndWeights', # lines of arrays
        ]

class Read_HSD: 

    def __init__(self, fname = 'dftb_in.hsd'):
        self.hsdf = open(fname, 'r')
        self.keypath = []
        self.keywords_dict = {}
        self.curr_dict = self.keywords_dict

    def nest_keys(self): # recursive build nested-key
        while True:
            line = self.hsdf.readline()
            if '{' in line: # dict depth forward
                sys.stdout.write(line[:-1]+ '    # DEPTH FORWARD\n')
                try: # key has attribute
                    key = line[0:line.index('=')].strip()
                except ValueError: # key without attribute
                    key = line[0:line.index('{')].strip()
                self.curr_dict = dict_from_path(self.keypath, self.keywords_dict) 
                self.curr_dict[key] = {} # initialize new key:dictionary
                self.keypath.append(key)
                self.curr_dict = self.curr_dict[key] # forward 1 depth
                #print(self.keypath, '   # AFTER FORWARD')
                if key in special_keys: # call function read special blocks
                    getattr(self, 'read_'+key.lower())
                self.nest_keys() 
            elif '=' in line: # Normal key 
                sys.stdout.write(line[:-1]+'    # Normal KEY-VALUE\n')
                pass
            elif '}' in line: # dict depth backward, break current recursion
                sys.stdout.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                #print(self.keypath, '   # AFTER BACKWARD')
                break
            elif not line: # Meet EOF
                sys.stdout.write('# MEET EOF')
                break
            elif line.strip() =='': # Blank line, don't put this before EOF
                sys.stdout.write('    # BLANK LINE\n')
                pass
            else:
                sys.stdout.write(line[:-1]+'    # NOT ASSIGNED CONDITION!!\n')
                pass

    def read_kpointsandweights(self):
        while True:
            line = self.hsdf.readline()
            if '}' in line: # dict depth backward
                sys.stdout.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                break

    def read_projectstates(self):
        while True:
            line = self.hsdf.readline()
            if '}' in line: # dict depth backward
                sys.stdout.write(line[:-1]+ '    # DEPTH BACKWARD\n')
                del self.keypath[-1] # backward 1 depth
                break

    def get_keydict(self):
        self.nest_keys()
        return self.keywords_dict

def dict_from_path(keypath, dictroot): 
    '''
    Auxiliary function locate to a depth of nested dictionary
    with path indicated by keypath list.
    '''
    d = dictroot
    for key in keypath:
        d = d[key]
    return d

def write_hsd(keywords_dict, hsdf, indent=0):
    for key, value in keywords_dict.items():
        hsdf.write('\t'*indent + key + '\n')
        if isinstance(value, dict):
            write_hsd(value, hsdf, indent+1)
        else:
            hsdf.write('\t'*indent + key+': '+str(value) + '\n')


