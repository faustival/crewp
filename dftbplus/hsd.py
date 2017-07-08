
def read_hsd(fname = 'dftb_in.hsd'): 
    global curr_dict
    hsdf = open(fname, 'r')
    inp = {}
    keypath = []
    curr_dict = inp
    def nest_keys(hsdf): # recursive build nested-key
        global curr_dict
        while True:
            line = hsdf.readline()
            if not line: # Meet EOF
                break
            elif '}' in line: # break current recurse, find parent dictionary
                del keypath[-1]
                curr_dict = dict_from_path(keypath, inp) # backward 1 depth
                print( 'KEYPATH: ', keypath)
                break
            elif line.strip() =='':
                print(line[:-1] + 'Blank line: ', )
                pass
            elif '{' in line: # meet recurse
                print(line[:-1] + 'Beginning new dict: ', )
                try: # key has attribute
                    key = line[0:line.index('=')].strip()
                except ValueError: # key without attribute
                    key = line[0:line.index('{')].strip()
                curr_dict[key] = {} # initialize new key:dictionary
                keypath.append(key)
                curr_dict = dict_from_path(keypath, inp) # forward 1 depth
                print( 'KEYPATH: ', keypath)
                nest_keys(hsdf) 
            else:
                print(line[:-1] + '  Normal key: ', )
    nest_keys(hsdf)
    print(inp)
    return inp

def dict_from_path(keypath, dictroot):
    d = dictroot
    for key in keypath:
        d = d[key]
    return d

special_keys = [ 'ProjectStates' ]


