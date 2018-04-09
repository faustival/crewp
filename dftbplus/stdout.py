
import re
import subprocess

def get_converged_energy(fname):
    '''
    Try to retrieve and return converged value of total energy
    from geometrical optimization calculation.
    If calculation is checked to be converged GeoOpt,
        a float value is returned, in the other case,
        the file name and the last line will be printed.
    '''
    last_line = subprocess.check_output(['tail', '-1', fname])
    if str(last_line, 'utf-8').strip()=='Geometry converged':
        with open(fname, 'r') as stdoutf:
            for line in stdoutf:
                m = re.match('.*Total Energy:', line)
                if m:
                    val = float( line[m.end():].split()[-2] )
        return val
    else: # GeoOpt Not converged or not GeoOpt calculation.
        print(fname, last_line)
