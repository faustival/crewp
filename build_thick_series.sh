#! /bin/bash

echo "Building thickness testing files"

workdir=/home/jinxi/pwjobs/au_surf_proj_dos/
maxthick=17
incr=2
minthick=9
jobprefx=au110_lyr
samplefile_scf=au110.scf.in

cd $workdir

for (( i=$maxthick; i>=$minthick; i-=$incr ))
do
  echo "building thickness $i"
  itrdir=$jobprefx$i
  mkdir $itrdir
  cp $samplefile_scf $itrdir
done



