#! /usr/bin/env python3

# 1. Read cartesian coordinates from Gaussian standard orientation output.
# 2. Read normal mode from high-precision type of frequency calc output.
# 3. Generate Gaussian input of PES scan along normal mode. 
# ( ONLY 1-dimensional now )
###################################

import numpy as np

def scan_pes_infgen(gaus_oput_file, gaus_scan_file, if_pseudogen, if_inverse_dx, n_atom, i_mode, n_grid, pe_hlevel, modes_in_line, mem, ncpu):

    ##########################################################################   
    # Basic variables:
    #   n_atom          : total number of atoms
    #   modes_in_line   : in high precision section of Gaussian output,
    #                     number of mode columns 
    #   i_mode          : which mode to scan
    #   n_grid          : for even number, zero point incorporated
    #   pe_hlevel       : pes scan up to which harmonic level 
    #   x0              : atomic Cartesian coordinates of optimized geometry
    #   dx              : eigenvector of i_mode displacement,
    #                     read from gaussian hpmode section
    #   omg0            : read harmonic frequency, in wavenumber unit
    #   mass            : atomic mass, has same dimension with x0 and dx
    #   scale_dx        : scaling of Cartesian displacement:
    #                     dx_max = dx * scale_dx
    #   dx_max          : maximum displacement after scaling,
    #                     default scan [-dx_max, dx_max]
    #   ddx             : separation of each Cartesian coord grid
    #   if_pseudogen    : =1 if write Pseudo=Read for heavy metals
    #   if_inverse_dx   : should only be 1 (inverse) or 0 (no inversion)    
    # All numerical calc. in atomic units
    ##########################################################################

    elements = []
    x0 = np.zeros(n_atom*3)
    dx = np.zeros(n_atom*3)
    mass = np.zeros(n_atom*3)
    
    wvnum2au=4.556333456861E-6
    amu2au=1822.888530
    bohr2a=0.529177
    
    atom = {
       1 : { 'name' : 'H ', 'mass' : 1.00794  },
       6 : { 'name' : 'C ', 'mass' : 12.0107  },
       8 : { 'name' : 'O ', 'mass' : 15.9994  },
      17 : { 'name' : 'Cl', 'mass' : 35.453   },
      47 : { 'name' : 'Ag', 'mass' : 107.8682 }
    }
    
    #################################################
    # the following are required for locating the critical strings 
    # for Gaussian output file reading.
    # list as follows:
    # 1. string name
    # 2. 1st character of the string locating at which column
    # 3. repeating time of locating the character
    #################################################
    gaus_loc_strs = {
    
      'hpc_rout' : {
        'tag' : 'Entering Link 1' ,
        'init' : 1 ,
        'itag' : 2
      } ,
    
      'hpc_rout_1' : {
        'tag' : 'Link1:  Proceeding to internal job step number  2' ,
        'init' : 1 ,
        'itag' : 1
      } ,
    
      'coord0':{
        'tag' : 'Standard orientation:' ,
        'init' : 25 ,
        'itag' : 1
      } ,
    
      'begin_hpc' : {
        'tag' : 'and normal coordinates:' ,
        'init' : 1 ,
        'itag' : 1
      } ,
    
      'hpc_freq' : {
        'tag' : 'Frequencies ---' ,
        'init' : 7 ,
        'itag' : 1
      } ,
    
      'hpc_dx' : {
        'tag' : 'Coord Atom Element:' ,
        'init' : 1 ,
        'itag' : 1
      } 
    }
    
    #################################################
    
    # function writing gaussian PES scan input file
    def wrtgaus(wrtfile,wrtcoord,wrtq_abs,wrtelements,cyctag,natoms,if_wrtpseudo) :
      count_atom = 0
      wrtfile.write('--link1--\n')
      wrtfile.write('%chk=h2o_scan_'+('%03d'%i_mode)+'.chk\n')
      #wrtfile.write('%mem='+('%d'%mem)+'gb\n')
      wrtfile.write('%nproc='+('%d'%ncpu)+'\n')
    #  wrtfile.write('#T ub3lyp/Gen Pseudo=Read Test\n')
      wrtfile.write('#P ub3lyp/Gen Freq=Raman NoSymmetry Test\n')
      wrtfile.write('\n')
      wrtfile.write('scan grid energy %i ttaagg, q = %f\n' %(cyctag, wrtq_abs))
      wrtfile.write('\n')
    #  wrtfile.write('0  2\n')
      wrtfile.write('0  1\n')
      while count_atom < natoms :
        wrtfile.write('%6s %16.8f %16.8f %16.8f\n' %(wrtelements[count_atom], wrtcoord[3*count_atom], wrtcoord[3*count_atom+1], wrtcoord[3*count_atom+2]))
        count_atom = count_atom + 1
      wrtfile.write('\n')
      wrtfile.write('O H 0\n')
      wrtfile.write('6-311+G**\n')
      wrtfile.write('****\n')
      if if_wrtpseudo==1 :
        wrtfile.write('Ag 0\n')
        wrtfile.write('LanL2DZ\n')
        wrtfile.write('****\n')
        wrtfile.write('\n')
        wrtfile.write('Ag 0\n')
        wrtfile.write('LanL2DZ\n')
      wrtfile.write('\n')
    
    # function locating the critical strings:
    def locate_line(file_in,str_break,counter_max,i_init_str,i_finl_str) :
      counter = 0
      while True:
        line = file_in.readline()
        if not line: 
          break
        if line[i_init_str:i_finl_str] == str_break :
          #print(line[i_init_str:i_finl_str])
          counter = counter + 1
          #print(counter)
          if counter == counter_max :
            #print(counter)
            break
      return line
    
    # calling locate_line and a short form for gaussian09 dictionary
    def locate_gaus_str(gaus_dict_key) :
        gaus_line_str = locate_line(infile, gaus_loc_strs[gaus_dict_key]['tag'], gaus_loc_strs[gaus_dict_key]['itag'], gaus_loc_strs[gaus_dict_key]['init'], (gaus_loc_strs[gaus_dict_key]['init'] + len(gaus_loc_strs[gaus_dict_key]['tag'])))
        return gaus_line_str

    infile = open(gaus_oput_file,'r')

    # locate Gaussian Link of frequency-Raman
    locate_gaus_str('hpc_rout_1')
    
    # locate Gaussian PES minimum coordinate 
    locate_gaus_str('coord0')
    
    # read PES minimum coordinates
    i = -4
    while i < n_atom :
      coord0_line = infile.readline()
      if i >= 0 :
        words = coord0_line.split()
        elements.append(words[1])
        for j in range(0,3) :
          mass[3*i+j] = atom[int(words[1])]['mass']
          x0[3*i+j] = words[3+j]
      i = i + 1
    #print 'N of elements, ', len(elements)
    #print 'elements = ', elements
    #print 'mass = ', mass
    #print 'x0 = ', x0 
    
    # locate high-precision freq section
    locate_gaus_str('begin_hpc')
    
    # locate and read high-precision frequency
    i = 0
    while i<=((i_mode-1)//modes_in_line) :
      freqline = locate_gaus_str('hpc_freq')
      #print(freqline)
      if i == (i_mode-1)//modes_in_line :
        words = freqline.split()
        omg0 = float(words[2+(i_mode-1)%modes_in_line])
        print('Mode No. = ', i_mode, 'HPC_Freq = ', omg0)
        # locate high-precision mode eigenvector displacement
        locate_gaus_str('hpc_dx')
        # read eigenvectors
        j = 0
        while j < n_atom*3 :
          eig0_line = infile.readline()
          words = eig0_line.split()
          dx[j] = words[3+(i_mode-1)%modes_in_line]
          j=j+1
        #print(dx)
      i=i+1

    # transform to atomic units
    omg_au = omg0*wvnum2au
    dx_au = dx/bohr2a
    mass_au = mass*amu2au
    
    # evaluate the maximum displacement constant relative to dx
    dq_sq = 0.
    i = 0
    while i<n_atom*3 :
      dq_sq = dq_sq + mass_au[i] * dx_au[i]**2 
      i = i+1
    scale_dx = np.sqrt( (2.*float(pe_hlevel)+1.) / omg_au / dq_sq  )
    #print(scale_dx)
    
    # inverse the scanning direction
    if if_inverse_dx==1 :
      dx_max = scale_dx * dx * (-1.)
    elif if_inverse_dx==0 :
      dx_max = scale_dx * dx 
    else :
      print '!!!CRITICAL ERROR, if_inverse_dx value!!!'
      exit()
    
    ddx = 2.*dx_max / float(n_grid)
    dq_max = scale_dx * np.sqrt(dq_sq)
    ddq = 2.*dq_max / float(n_grid)
    
    #print 'ddx =', ddx
    #print 'dq_max =', dq_max
    
    # write to PES scan file
    scan_file = open(gaus_scan_file,'w')
    i = 0
    while i<(n_grid+1) :
      # write the single point energy part:
      wrtgaus(scan_file,(x0-dx_max+float(i)*ddx),(-dq_max+float(i)*ddq),elements,i+1,n_atom,if_pseudogen)
      i=i+1
    
    infile.close()
    scan_file.close()
    
    # output frequency to check imaginary
    return omg0



