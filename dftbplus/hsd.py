
def read_hsd(fname = 'dftb_in.hsd'): 
    global curr_dict
    hsdf = open(fname, 'r')
    keywords_dict = {}
    keypath = []
    curr_dict = keywords_dict
    def nest_keys(hsdf): # recursive build nested-key
        global curr_dict
        while True:
            line = hsdf.readline()
            if not line: # Meet EOF
                break
            elif '}' in line: # break current recurse, find parent dictionary
                del keypath[-1]
                curr_dict = dict_from_path(keypath, keywords_dict) # backward 1 depth
                break
            elif line.strip() =='': # Blank line
                pass
            elif '{' in line: # meet recurse
                try: # key has attribute
                    key = line[0:line.index('=')].strip()
                except ValueError: # key without attribute
                    key = line[0:line.index('{')].strip()
                curr_dict[key] = {} # initialize new key:dictionary
                keypath.append(key)
                curr_dict = dict_from_path(keypath, keywords_dict) # forward 1 depth
                nest_keys(hsdf) 
            else: # Normal key 
                pass
    nest_keys(hsdf)
    return keywords_dict

def dict_from_path(keypath, dictroot):
    d = dictroot
    for key in keypath:
        d = d[key]
    return d

special_keys = [ 'ProjectStates' ]

def write_hsd(keywords_dict, hsdf, indent=0):
    for key, value in keywords_dict.items():
        print('\t'*indent + key)
        if isinstance(value, dict):
            write_hsd(value, hsdf, indent+1)
        else:
            print('\t'*indent + key+': '+str(value))
