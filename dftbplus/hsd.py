


def read_hsd(fname = 'dftb_in.hsd'): 
    hsdf = open(fname, 'r')
    inp = {}
    keypath = []
    curr_dict = inp
    def nest_keys(hsdf): # recursive build nested-key
        while True:
            line = hsdf.readline()
            if not line: 
                print('Meet EOF')
                break
            elif '}' in line: # break current recurse, find parent dictionary
                print(line[:-1] + 'End of current dict: ', )
                #del keypath[-1]
                break
            elif line.strip() =='':
                print(line[:-1] + 'Blank line: ', )
            elif '{' in line: # meet recurse
                print(line[:-1] + 'Beginning new dict: ', )
                #new_dict_line(line)
                nest_keys(hsdf) 
            else:
                print(line[:-1] + '  Normal key: ', )
    nest_keys(hsdf)
    return inp

def dict_from_path(keypath):
    d = inp
    for key in keypath:
        d = d[key]
    return d

def new_dict_line(line):
    try: # key has 
        key = line[0:line.index('=')].strip()
    except ValueError:
        key = line[0:line.index('{')].strip()
    curr_dict[key] = {}
    keypath.append(key)
    curr_dict = dict_from_path(keypath)




