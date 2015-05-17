#! /usr/bin/python3

def read_lpdosf(inpfname, spin_pol):
    '''
    input file structure:
    <beginning of file>
    # E (eV)  ldosup(E)  ldosdw(E) pdosup(E)  pdosdw(E)  ...<$more>
     -6.759  0.944E-07  0.942E-07  0.944E-07  0.942E-07
     ...
     ...
    <end of file>
    <$more> = <more magnetic quantum number>

    INPUT:
        inpf:      input filename, 
        spin_pol:  True for spin-polarized
    OUTPUT:
        engy:      1-dim list, raw energy
        lpdos:      If spin-polarized: 
                       ([spin up array],[spin down array])
                   If not spin-polarized:
                       [lpdos array]
    '''
    inpf = open(inpfname,'r')
    engy = []
    if not spin_pol:
        lpdos = []
    elif spin_pol:
        lpdos = ([],[])
    while True:
        line = inpf.readline()
        if not line:
            break
        words = line.split()
        if words[0]=='#':
            continue
        else:
            engy.append( float(words[0]) )
            if not spin_pol:
                lpdos.append( float(words[1]) )
            elif spin_pol:
                lpdos[0].append( float(words[1]) )
                lpdos[1].append( float(words[2]) )
    inpf.close()
    return engy, lpdos

def read_pdos(file_prefx, atom_wfc_list, spin_pol):
    '''
    Input of atom_wfc_list like:
        [
          ('1','O' ,['s','p']     ),
          ('2','Au',['s','p','d'] ),
          ...
        ]
    Returns the pdos:
        [
          ('1','O' ,[['s',lpdos],['p',lpdos]]             ),
          ('2','Au',[['s',lpdos],['p',lpdos],['d',lpdos]] ),
          ...
        ]
    Where `lpdos` read from function `read_lpdosf`.
    '''
    orbital_dict = { 's':'1', 'p':'2', 'd':'3', 'f':'4' }
    pdos = []
    for (atom_id, atom, wfc_list) in atom_wfc_list:
        pdos_list = []
        for wfc in wfc_list:
            lpdos_fname = file_prefx + '.pdos_atm#' + atom_id + \
                              "(" + atom + ')_wfc#' + \
                              orbital_dict[wfc] + '(' + wfc + ')'
            engy, lpdos = read_lpdosf(lpdos_fname, spin_pol)
            pdos_list.append([wfc, lpdos]) 
        pdos.append( (atom_id, atom, pdos_list) )
    return engy, pdos

