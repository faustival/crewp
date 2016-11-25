#! /usr/bin/env python3

# scanning Gaussian ouput file for PES, dipole, polarizability
# ( ONLY 1-dimensional now )
###################################
#
# Basic variables:
#   if_inverse_dx   : -1. to inverse the scanning direction


import numpy as np
import re
import sys

def readpes(gaus_scan_ofile, pes_file, if_inverse_q, n_grid) :

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#!!! be CAREFUL, temporary only symmetric scan is effective for if_inverse !!!
# if_inverse_q  : should only be 1 (inverse) or 0 (no inversion)
# n_grid        : for odd number, zero point incorporated
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    q = np.zeros(n_grid+1)
    en = np.zeros(n_grid+1)
    i_grid = np.zeros(n_grid+1)
    dipole_3dim = np.zeros((n_grid+1,3))
    polar_6dim = np.zeros((n_grid+1,6))
    hypol_10dim = np.zeros((n_grid+1,10))
    '''
    according to Gaussian 09 manual, ~Freq~ keyword, example of #P output
    the sequence of polarizability tensor:
    xx, xy, yy, xz, yz, zz
    '''
    
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
        'itag' : 1
      } ,
    
      'scan_tag':{
        'tag' : 'scan grid energy' ,
        'init' : 1 ,
        'itag' : 1
      } ,
    
      'scf_en' : {
        'tag' : 'SCF Done:' ,
        'init' : 1 ,
        'itag' : 1
      } ,
     
      'hiprec_dipole' : {
        'tag' : 'Dipole        =' ,
        'init' : 1 ,
        'itag' : 1
      }, 
     
      'hiprec_polar' : {
        'tag' : 'Polarizability=' ,
        'init' : 1 ,
        'itag' : 1
      }, 
     
      'hiprec_hypol' : {
        'tag' : 'HyperPolar    =' ,
        'init' : 1 ,
        'itag' : 1
      } 
    }
    
    #################################################
    
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
          if counter == counter_max :
            break
      return line

    # calling locate_line and a short form for gaussian09 dictionary
    def locate_gaus_str(gaus_dict_key) :
        gaus_line_str = locate_line(infile, gaus_loc_strs[gaus_dict_key]['tag'], gaus_loc_strs[gaus_dict_key]['itag'], gaus_loc_strs[gaus_dict_key]['init'], (gaus_loc_strs[gaus_dict_key]['init'] + len(gaus_loc_strs[gaus_dict_key]['tag'])))
        return gaus_line_str
    
    # function transform Gaussian Raman polarizability string to 3-dim array
    def trans_response_ary(raw_str) :
        raw_str = re.sub('D','e',raw_str)
        if ((len(raw_str))%15) != 0:
            print('Reading polarizability raw string, error!')
            sys.exit()
        dim_rsp_ary = len(raw_str)//15
        rsp_ary = []
        for i in range(0,dim_rsp_ary) :
            rsp_ary.append(raw_str[(i*15):(i+1)*15])
        return rsp_ary
    
    # read gaussian static electric response
    def read_gser(rsp_dictkey, dim_red_tensor) :
        # rsp_dictkey: string matching key in dictionary for response function
        # dim_red_tensor: dimension of reduced response tensor
        if dim_red_tensor < 3 :
            print('Electric static response, dimension > 3!')
            exit() 
        n_total_line = (dim_red_tensor+2)//3
        dim_last_line = (dim_red_tensor-1)%3+1
        response = []
        for i in range(1, n_total_line+1) :
            if i==1 :
                # locate the key in dictionary, then always read the first 3 entries
                response_line = locate_gaus_str(rsp_dictkey)
                response_raw_str = response_line[16:61]
            elif i>1 :
                response_line = infile.readline()
                if i<n_total_line :
                    response_raw_str = response_line[16:61]
                elif i==n_total_line :
                    response_raw_str = response_line[16:(16+15*dim_last_line)]
            response.extend(trans_response_ary(response_raw_str))
        return response
            
        
    infile = open(gaus_scan_ofile,'r')
    ofile = open(pes_file,'w')
    
    # begin iterating PES grids
    i = 0
    while i<=n_grid :
      #print '\nGRID INDEX NO.',i
      # locate tag for each scanning grid
      tag_line = locate_gaus_str('scan_tag')
      words = tag_line.split()
      q[i] = words[7]
      i_grid[i] = words[3]
      # read single point SCF energy
      scf_line = locate_gaus_str('scf_en')
      words = scf_line.split()
      en[i] = words[4]
      #print scf_line
      # read high precision Raman electronic polarizability
      dipole_3dim[i,:] = read_gser('hiprec_dipole', 3)
      polar_6dim[i,:] = read_gser('hiprec_polar', 6)
      hypol_10dim[i,:] = read_gser('hiprec_hypol', 10) 
      #print 'dipole_3 = ', dipole_3dim[i,:]
      #print 'polar_6 = ', polar_6dim[i,:]
      #print 'hyperpol_10 = ', hypol_10dim[i,:]
      i = i+1
    
    # reverse the coordinate direction
    if if_inverse_q==1 :
      en = en[::-1]
    elif if_inverse_q==0 :
      print('No coordinate inversion.')
    else :
      print('!!!CRITICAL ERROR, if_inverse_q value!!!')
      exit()
    
    #print 'q = ', q
    #print 'en = ', en
    #print 'grid counting', i_grid
    
    # list PES in file
    ofile.write('%5s %16s %16s\n' %('Grid', '|q|', 'En'))
    i = 0
    while i<=n_grid :
      ofile.write('%5d %16.8f %16.8f\n' %(i_grid[i], q[i], en[i]))
      i = i+1
    
    infile.close()
    ofile.close()
    
    return q, en, i_grid, dipole_3dim, polar_6dim, hypol_10dim
    


