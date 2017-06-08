
import re
import numpy as np

def rlx_step(carfname='OSZICAR'):
    carf = open(carfname, 'r')
    en_steps = []
    while True:
        line = carf.readline()
        if not line: break
        if re.search('F= ', line):
            words = line.split()
            en_steps.append( np.array( [words[2], words[4]] ) )
    en_steps = np.array(en_steps)
    return en_steps
