#! /usr/bin/python3


def read_pwchrg(inpfname):
    '''
    read the header of plain text file
    /flib/plot_io.f90 subroutine plot_io()
    '''
    inpf = open(inpfname, 'r')
    # title
    line = inpf.readline()
    # grid number
    line = inpf.readline()
    words = line.split()
    [nr1x, nr2x, nr3x, nr1, nr2, nr3, nat, ntyp] = words.copy()
    print(nr1x,nat)




inpfname = 'ag100chrg.log'
read_pwchrg(inpfname)


