#! /usr/bin/python3

workpath = '/home/jinxi/pwjobs/au_surface_proj/au111_lyr5/'

inf = 'au111.pdos.plot.pdos_atm#1(Au)_wfc#3(d)'

print(inf,workpath)

def read_pdosf(inpf,spin)
    while True:
        line = inpf.readline()
        if not line:
            break
        words = line.split()
        if words[0]=='#':
            continue
        return pdos



