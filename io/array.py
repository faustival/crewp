
import numpy as np
import sys
import builtins

def auto_fmt(entry):
    '''
    Automatically determine the proper format when writing a homogeneous array-like datastructure by the type of entries in the array. ( e.g., pass in entry=list[0][0], entry=numpy.ndarray[0,0,0], ... )
    '''
    if isinstance(entry, str) or ('str' in type(entry).__name__): 
        fmt='{:5s}'
    elif isinstance(entry, int) or ('int' in type(entry).__name__): 
        fmt='{:5d}'
    elif isinstance(entry, float) or ('float' in type(entry).__name__): 
        fmt='{:13.8f}' 
    else: sys.exit("In ``auto_fmt``, auto type search for: "+str(entry)+", No proper type found!")
    return fmt

def wrt_1darry(
        arry1d,
        f=sys.stdout, # file for writing
        rowtag='',  # tag before data
        fmt='',
        fmt_tag='',
        lmargin=2, # width of left margin
        sep=' ', # separation between entries
        col_lim=None, # limit column number
        ):
    if rowtag: 
        if not fmt_tag: 
            # automatic determine type and format of rowtag
            fmt_tag = auto_fmt(rowtag)
        rowtag = fmt_tag.format(rowtag)
    else: rowtag = ''
    if not fmt: 
        # automatic determine format by type of 1st entry of arry2d
        fmt = auto_fmt(arry1d[0])
    # write 1-dimensional array 
    if (not col_lim) or (len(arry1d)<=col_lim): # use simple 1-line form
        f.write( ' '*lmargin+rowtag+sep.join( [fmt.format(entry) for entry in arry1d] )+'\n' )
    else: # split into multiple lines
        for i_row in range( len(arry1d)//col_lim ):
            if i_row==0: # first row, write ``rowtag``
                arry_in_line = arry1d[ : col_lim]
                f.write( ' '*lmargin+rowtag+sep.join( [fmt.format(entry) for entry in arry_in_line] )+'\n' )
            else: # 2 ~ [nrow-1] rows, turn rowtag as blank
                arry_in_line = arry1d[i_row*col_lim : (i_row+1)*col_lim]
                rowtag = len(rowtag)*' '
                f.write( ' '*lmargin+rowtag+sep.join( [fmt.format(entry) for entry in arry_in_line] )+'\n' )
        remainder = len(arry1d) % col_lim
        if remainder != 0: # last row
            arry_in_line = arry1d[ -remainder : ]
            rowtag = len(rowtag)*' '
            f.write( ' '*lmargin+rowtag+sep.join( [fmt.format(entry) for entry in arry_in_line] )+'\n' )

def wrt_2darry( 
        arry2d,  #2-dimensional array
        f=sys.stdout, # file for writing
        title='',  # title line
        rowtags=None,  # tag of rows, see full comments
        fmt='',
        fmt_tag='',
        lmargin=2, # width of left margin
        sep=' ', # separation between entries
        col_lim=None, # limit column number
        ):
    '''
    Automatic choice: only pass in arry2d and file to be written. (useful in checking data.)
    Printing 2-dimensional array, i.e., matrix
    rowtags: should be none, or sequence match row number of arry2d 
    '''
    if title:
        f.write(title+'\n')
    if rowtags and not fmt_tag: 
        # automatic determine type and format of rowtag
        fmt_tag = auto_fmt(rowtags[0])
    if not fmt: 
        # automatic determine format by type of 1st entry of arry2d
        fmt = auto_fmt(arry2d[0][0])
    # write 2-dimensional array 
    for i, arry1d in enumerate(arry2d): 
        if rowtags: rowtag = fmt_tag.format(rowtags[i])
        else: rowtag = ''
        wrt_1darry(arry1d, f, rowtag, fmt, fmt_tag, lmargin, sep, col_lim )

def wrt_3darry(arry3, title, f=sys.stdout):
    '''
    Printing 3-index array, only work for checking data now.
    '''
    f.write(title+'\n')
    for i, arry2d in enumerate(arry3):
        arry2dtitle = 'Inner matrix of 3D-array : '+'{:d}'.format(i+1)
        wrt_2darry(arry2d, arry2dtitle, f=f)

def read_2darry( f, nrow='auto', typefunc='float', ):
    '''
    Call after locate to the first aligned line!
    '''
    arry = []
    if nrow=='auto': # get the pattern from 1st line
        while True:
            words = f.readline().split()
            if not arry: # first vector line
                veclen = len(words)
            elif arry: 
                if len(words) != veclen: # break if length not match
                    break
            try:
                arry.append( [ getattr(builtins, typefunc)(entry) \
                         for entry in words ] )
            except ValueError: # break for row pattern not match
                break
    else: # iterating over row number
        for i in range(nrow):
            words = f.readline().split()
            arry.append( [ getattr(builtins, typefunc)(entry) \
                     for entry in words ] )
    return np.array(arry)
