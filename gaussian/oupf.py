
import sys
import re
import numpy as np

def get_line(oupf, re_method, regex):
    '''
    Use to compress the code,
    jump to a line meeting RegEx and return line.
    '''
    while True:
        line = oupf.readline()
        if not line: break
        if getattr(re, re_method)(regex, line): 
            break
    return line

class Oupf: 
    '''
    I creep over output few times,
    because of the messy organization of output.
    '''
    def __init__(self, fname):
        self.fname = fname
        # Read over once and find all links and route section.
        self.get_link_route()
        # Delete all below after test:
        self.get_vib_auto()

    def get_link_route(self, read_route=True):
        '''
        Finding line-NO. of all 'Entering Link 1' tag
        and all corresponding input route section 
        ( routes automatically generated were passed away ).
        '''
        self.link_line_no = [] # line NO.s of 'Entering Link 1'
        self.route_line_no = [] # line NO.s of route section
        self.route_line = [] # Strings of route section
        oupf = open(self.fname, 'r')
        for i, line in enumerate(oupf, 1): 
            '''
            Counting line number in iteration, 
            DON'T add loops anymore.
            '''
            if 'Entering Link 1' in line:
                self.link_line_no.append(i)
            if read_route and re.match('^\s*#', line):
                if ( len(self.route_line) == len(self.link_line_no) - 1 ):
                    self.route_line_no.append(i)
                    self.route_line.append(line)
        oupf.close()

    def get_vib(self, ilink=0):
        '''
        Get the results of Vibrational spectrum
        in i-th 'Entering Link 1'.
        '''
        oupf = open(self.fname, 'r')
        # Jump to the route line of i-th 'Entering Link 1'.
        for i in range(self.route_line_no[ilink]):
            oupf.readline()
        # Find degree of freedom
        degline = get_line(oupf, 'search', 'Deg. of freedom')
        print(degline)
        oupf.close()

    def get_vib_auto(self):
        '''
        Find the ONLY Link for vibrational calc.
        And call method to read. 
        Only execute in case of only 1 vibrational calc. 
        Or print error.
        '''
        freq_routes = []
        # check all route section to find if the ONLY 'freq' job
        for i, line in enumerate(self.route_line):
            if re.search('freq', line, re.IGNORECASE):
                freq_routes.append(i)
                if len(freq_routes) > 1: # Case: not ONLY 1 'freq' job.
                    sys.exit("At least 2 'freq' job in output:", self.fname)
                    break
        if not freq_routes: # Case: NO 'freq' job found.
            sys.exit("'freq' job NOT found in output:", self.fname)
        freq_route_no, = freq_routes # Case: found the only 1 'freq' job.
        print("The only 'freq' job:", freq_route_no)
        # Call method to read vibrational info.
        self.get_vib(freq_route_no)

    def get_template(self):
        '''
        A template for creeping over oupf line by line
        '''
        oupf = open(self.fname, 'r')
        while True:
            line = oupf.readline()
            if not line: break
        oupf.close()



