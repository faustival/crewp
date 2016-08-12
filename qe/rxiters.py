
import re

class rxIters:

    def __init__(self, oupfname):
        self.oupfname = oupfname

    def rxconv(self):
        '''
        Reading total energies and force from
        each cycles of geometric opt.
        '''
        self.enseq = []
        self.forcseq = []
        with open(self.oupfname, 'r') as oupf:
            while True:
                line = oupf.readline()
                # search total energy conv
                if re.search('!', line):
                    words = line.split()
                    self.enseq.append(float(words[4]))
                # compute stepwise total energy diff 
                self.endiff = [ self.enseq[i] - self.enseq[i-1] for i in range(1, len(self.enseq)) ]
                self.endiff = [0.0] + self.endiff
                # search total force conv
                if re.search('Total force', line):
                    words = line.split()
                    self.forcseq.append(float(words[3]))
                if not line:
                    break
        self.iterseq = [i for i in range(1, len(self.enseq)+1)]

    def printconv(self):
        print('{0:>10s} {1:>10s} {2:>18s}'.format('Iter', 'Force', 'Energy'))
        for i in range(len(self.iterseq)):
            print('{0:10d} {1:10.4f} {2:18.8f}'.format(self.iterseq[i], self.forcseq[i], self.enseq[i]))


