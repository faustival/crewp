
def read_table( f, nrow='auto', ):
    '''
    Call after locate to the first aligned line!
    '''
    table = []
    if nrow=='auto': # get the pattern from 1st line
        while True:
            words = f.readline().split()
            if not table: # first vector line
                rowlen = len(words)
            elif table: 
                if len(words) != rowlen: # break if length not match
                    break
            table.append( words )
    else: # iterating over row number
        for i in range(nrow):
            words = f.readline().split()
            table.append( words )
    return table
