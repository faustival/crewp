
def new_dict_line(line):
    try: # key has 
        key = line[0:line.index('=')]
        print(key)
    except ValueError:
        key = line[0:line.index('{')]
        print(key)

def nest_keys(hsdf):
    while True:
        line = hsdf.readline()
        if not line: break
        if '{' in line: # new nested dictionary
            new_dict_line(line)
            nest_keys(hsdf)
        else:
            print(line)

def read_hsd(fname = 'dftb_in.hsd'):
    hsdf = open(fname, 'r')
    nest_keys(hsdf)

