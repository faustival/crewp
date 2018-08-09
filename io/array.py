
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
    else: sys.exit("In ``auto_fmt``, auto type search for: "+str(arry2[0][0])+", No proper type found!")
    return fmt

def wrt_2darry( 
        arry2,  #2-dimensional array
        f=sys.stdout, # file for writing
        title='',  # title line
        rowtags=None,  # tag of rows, see full comments
        fmt='',
        fmt_tag='',
        lmargin=' ', # left margin
        sep=' ', # separation between entries
        ):
    '''
    Automatic choice: only pass in arry2 and file to be written. (useful in checking data.)
    Printing 2-dimensional array, i.e., matrix
    rowtags: should be none, or sequence match row number of arry2 
    '''
    if title:
        f.write(title+'\n')
    if rowtags and not fmt_tag: 
        # automatic determine type and format of rowtag
        fmt_tag = auto_fmt(rowtags[0])
    if not fmt: 
        # automatic determine format by type of 1st entry of arry2
        fmt = auto_fmt(arry2[0][0])
    # write 2-dimensional array 
    for i, vec in enumerate(arry2): 
        if rowtags: rowtag = fmt_tag.format(rowtags[i])
        else: rowtag = ''
        f.write( lmargin+rowtag+sep.join( [fmt.format(entry) for entry in vec] ) )
        f.write('\n')

def wrt_3darry(arry3, title, f=sys.stdout):
    '''
    Printing 3-index array
    '''
    f.write(title+'\n')
    for i, arry2 in enumerate(arry3):
        arry2title = 'Inner matrix of 3D-array : '+'{:d}'.format(i+1)
        wrt_2darry(arry2, arry2title, f=f)

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
