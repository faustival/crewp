#! /usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.nan)

dosinpf = '/home/jinxi/pwjobs/cyan_ads/au3pd_brg_molproj/plotprojmo.mopdos'

nstate = 40

data = pd.read_csv(dosinpf, delim_whitespace=True, comment='#', index_col=0, header=None, names=['engy','dos'])

# reform this use Hierarchical indexing and Reshaping 

enary = data.ix[1]['engy'].values

pdosmat = [data.ix[i]['dos'].values for i in range(1,nstate+1)]


for i in range(0,nstate):
    plt.plot(enary, pdosmat[i])

plt.show()


