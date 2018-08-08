
import numpy as np
import sys
import builtins

def wrt_2darry( 
        arry2,  #2-dimensional array
        title='',  # title line
        rowtags='',  # tag of rows, see full comments
        f=sys.stdout, # file for writing
        wtype='',
        fmt='',
        lmargin=' ', # left margin
        sep=' ', # separation between entries
        ):
    '''
    Printing 2-dimensional array, i.e., matrix
    rowtags: should be none, or sequence match row number of arry2 
    '''
    if title:
        f.write(title+'\n')
    if rowtags: 
        # automatic determine type and format of rowtag
        if type(rowtags[0])==str: tagfmt = '{:5s}'
        elif type(rowtags[0])==int: tagfmt = '{:5d}'
    if not fmt: 
        # automatic determine format by type of 1st entry of arry2
        if wtype=='str' or isinstance(arry2[0][0], (str)): 
            fmt='{:5s}'
        elif wtype=='int' or isinstance(arry2[0][0], (int)): 
            fmt='{:5d}'
        elif wtype=='float' or isinstance(arry2[0][0], (float)): 
            fmt='{:13.8f}' 
        else: sys.exit("In ``wrt_2darry``, auto type search for: "+str(arry2[0][0])+", No proper type found!")
    # write 2-dimensional array 
    for i, vec in enumerate(arry2): 
        if rowtags: rowtag = tagfmt.format(rowtags[i])
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
