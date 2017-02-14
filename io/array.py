
import numpy as np
import sys

def wrt_2darry(arry2, title, rowtags='', f=sys.stdout):
    '''
    Printing 2-index array, i.e., matrix
    rowtags: should be none, or sequence match row number of arry2 
    '''
    f.write(title+'\n')
    if rowtags: # determine type and print format of rowtag
        if type(rowtags[0])==str: # treat tags as string
            tagfmt = '{:5s}'
        elif type(rowtags[0])==int:
            tagfmt = '{:5d}'
        for i, vec in enumerate(arry2): # iterating rows
            rowtag = tagfmt.format(rowtags[i])
            f.write( '   '+rowtag+' '.join( '{:13.8f}'.format(entry) for entry in vec ) )
            f.write('\n')
    elif not rowtags: # no row tags
        for vec in arry2: # iterating rows
            f.write( '   '+' '.join( '{:13.8f}'.format(entry) for entry in vec ) )
            f.write('\n')
    f.write('\n')

def wrt_3darry(arry3, title, f=sys.stdout):
    '''
    Printing 3-index array
    '''
    f.write(title+'\n')
    for i, arry2 in enumerate(arry3):
        arry2title = 'Inner matrix of 3D-array : '+'{:d}'.format(i+1)
        wrt_2darry(arry2, arry2title, f=f)

