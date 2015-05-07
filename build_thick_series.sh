#! /bin/bash

echo "Building thickness testing files"

workdir=/home/jinxi/pwjobs/au_surf_proj_dos/
maxthick=11
incr=2
minthick=1
jobprefx=au110_lyr
samplefile_scf=au110.scf.in
layersep=2.345

cd $workdir

for (( i=$maxthick; i>=$minthick; i-=$incr ))
do
  echo "building thickness $i"
  itrdir=$jobprefx$i
  mkdir $itrdir
  cp $samplefile_scf $itrdir
  modfile=$itrdir/$samplefile_scf
  # modify total atomic number
  sed -i -r "s/(nat=).*/\1$i,/" $modfile
  # find the line number of begining atomic coordinate 
  nln_coord=`sed -n '/ATOMIC_POSITIONS/=' $modfile`
  nln_del_start=`expr $nln_coord + $i`
  pttn_start=`sed -n "$nln_del_start p" $modfile`
  nln_del_limit=`sed -n '/K_POINTS/=' $modfile`
  echo Del start at $nln_del_start, limit at $nln_del_limit
  # check if thickness of sample file is enough
  if [ $nln_del_start -ge $nln_del_limit ]; then
    echo no enough layers in sample file
    exit 0
  fi
  # delete coordinate lines exclude patterns
  sed -i "/$pttn_start/,/K_POINTS/{//!d}" $modfile
  # calc the cell period of z-axis and replace 
  #   to cell parameter
  zcell=$(echo "20.0 + $layersep*$i"|bc)
  echo z-axis of cell,  $zcell
  nln_cellpar=`sed -n '/CELL_PARAMETERS/=' $modfile`
  nln_zcell=`expr $nln_cellpar + 3`
  ln_zcoord_old=`sed -n "$nln_zcell p" $modfile`
  ln_zcoord_new=`sed -e "s/[^ ]*[^ ]/$zcell/3" <<< $ln_zcoord_old`
  echo $ln_zcoord_new
  sed -i "${nln_zcell}s/[^ ].*/$ln_zcoord_new/" $modfile
done




