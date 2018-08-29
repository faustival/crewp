
import re

def float_from_re(fname, content, ):
    '''
    Temperorily run as:
    Get single float from one line from stdout.
        first truncate line to end of re.match pattern,
        assign float position in residue of splitted line.
    fill in content_dict for new content.
    '''
    content_dict = {
            'fermi': [ '^\s*Fermi Energy          =', -1 ] ,
            'fermi_Llead': [ '^\s*Lead  1 Fermi energy in Lead File =', -1 ] ,
            'fermi_Rlead': [ '^\s*Lead  2 Fermi energy in Lead File =', -1 ] ,
            'Potential_Llead': [ '^\s*Built-in Potential 1  =', -1 ] ,
            'Potential_Rlead': [ '^\s*Built-in Potential 2  =', -1 ] ,
            'fermi_Rlead': [ '^\s*Lead  2 Fermi energy in Lead File =', -1 ] ,
            'temperature': [ '^\s*Temperature :         ', -1 ] ,
            'ept_inelastic': [ '^\s*Steady state current\(inelastic LoE\) :', -2 ] ,
            }
    [re_key, position] = content_dict[content]
    with open(fname, 'r') as stdoutf:
        for line in stdoutf:
            m = re.match(re_key, line)
            if m:
                val = float( line[m.end():].split()[position] )
    return val

def get_typeinfo(fname):
    '''
    read TypeInfo section from header of stdout, with Element-max_angular pair into dictionary:
    { 
        'Au': 'd',
        'O' ; 'p',
        ...,
    }

    '''
    with open(fname, 'r') as stdoutf:
        for line in stdoutf:
            if '[TypeInfo]' in line:
                ntype = int(stdoutf.readline().split()[-1])
                chemsymbol_dict = {}
                for i in range(ntype):
                    words = stdoutf.readline().split()
                    chemsymbol_dict[words[3]] = words[-1]
    return chemsymbol_dict

def get_poissonbox(fname):
    '''
    Temporarily only grid number of Poisson Box is read.
    '''
    with open(fname, 'r') as stdoutf:
        for line in stdoutf:
            if '[Device Poisson Box]' in line:
                for _ in range(5):
                    stdoutf.readline()
                words = stdoutf.readline().split()
                gridsize = tuple( [ int(ni) for ni in (words[2], words[5], words[8]) ] ) # (nx, ny, nz)
    return gridsize
