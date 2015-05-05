#!/bin/bash

echo 'iteratively submitting cluster jobs!'

scanf_prefix='stark_scan_h2o_mode_'
jobexec=q09b
delay_time=1

for i in {001..003} ; do
    echo "iter No. $i"
    scan_gaus_inf=$scanf_prefix$i.com
    if [ -e $scan_gaus_inf ]; then
        $jobexec $scan_gaus_inf
        echo "file, $scan_gaus_inf", submitted
        sleep $delay_time
    else
        echo "!!, $scan_gaus_inf, not exist !!"
    fi
done



