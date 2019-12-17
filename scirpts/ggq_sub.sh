#!/bin/sh
for localSearch in  _SWAP _INSERT _TRI _VINSERT _None
do
echo localSearch = ${localSearch}
# for ins in 8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins 17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins 11_11_RANDOMCLUSTERED_CLUSTERED_MSVFLV_QUADRANT_thre0.1MPDAins
for ins in  17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins 11_11_RANDOMCLUSTERED_CLUSTERED_MSVFLV_QUADRANT_thre0.1MPDAins
do
echo ${ins}
if [ -d /vol/grid-solar/sgeusers/guanqiang/mpda_exp_data/$ins/ga_opt_$localSearch ]; then
    echo 'there is a dir for saving data'
else
    mkdir -p /vol/grid-solar/sgeusers/guanqiang/mpda_exp_data/$ins/ga_opt_$localSearch 
fi
qsub mpda_scripts.sh ${ins} ${localSearch}
done
done





    
