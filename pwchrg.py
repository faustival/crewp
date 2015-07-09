#! /usr/bin/python3

def get_words(inpf):
    line = inpf.readline()
    return line.split()

def lines2array(inpf,ncol):
    arry = []
    while True:
        words = get_words(inpf)
        if len(words)<ncol:
            break
        if len(words)>ncol:
            print('RESET the column number!')
            break
        else:
            rowary = [float(num) for num in words]
            arry.append(rowary) 
    return arry

def read_pwchrg(inpfname):
    '''
    read the header of plain text file
    /flib/plot_io.f90 subroutine plot_io()
    '''
    inpf = open(inpfname, 'r')
    # title
    words = get_words(inpf)
    # grid number, number of atom, number of atomic types
    words = get_words(inpf)
    nr1x, nr2x, nr3x, nr1, nr2, nr3, nat, ntyp = [int(nu) for nu in words.copy()]
    # ibrav and celldm
    words = get_words(inpf)
    ibrav = int(words[0])
    celldm = tuple([float(words[i]) for i in range(1,7)])
    if ibrav==0:
        cell = []
        for i in range(3):
            words = get_words(inpf)
            cellvec = tuple([float(nu) for nu in words]) 
            cell.append(cellvec)
    # energy cutoff, ...
    words = get_words(inpf)
    gcutm, dual, ecut = [float(words[i]) for i in range(3)]
    plot_num = int(words[3])
    # atom type list and valence charge
    zvalence = []
    for i in range(ntyp):
        words = get_words(inpf)
        zval = []
        zval.append(int(words[0]))
        zval.append(words[1])
        zval.append(float(words[2]))
        zval = tuple(zval)
        zvalence.append(zval)
    print(zvalence)
    # atomic positions
    atom_coord = []
    for i in range(nat):
        words = get_words(inpf)
        print(words)
    # charge density
    chrg1dary = lines2array(inpf,5)
    print('length of chrg1d', len(chrg1dary))
    inpf.close()

inpfname = 'ag100chrg.log'
read_pwchrg(inpfname)


