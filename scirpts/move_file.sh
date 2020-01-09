#!/bin/sh



    
for localSearch in  _SWAP _INSERT _TRI _None _TRISWAP
# for localSearch in  _None 
do
echo localSearch = ${localSearch}
# for ins in 
# 17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins
# 8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins 
# 17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins 11_11_RANDOMCLUSTERED_CLUSTERED_MSVFLV_QUADRANT_thre0.1MPDAins
for ins in 20_20_CLUSTERED_RANDOM_QUADRANT_LVSCV_thre0.1MPDAins 20_18_RANDOM_ECCENTRIC_QUADRANT_SVLCV_thre0.1MPDAins 8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins 17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins 11_11_RANDOMCLUSTERED_CLUSTERED_MSVFLV_QUADRANT_thre0.1MPDAins
# for ins in  17_23_RANDOMCLUSTERED_CLUSTERED_LVLCV_LVSCV_thre0.1MPDAins 11_11_RANDOMCLUSTERED_CLUSTERED_MSVFLV_QUADRANT_thre0.1MPDAins
do
echo ${ins}
if [ -d /vol/grid-solar/sgeusers/guanqiang/mpda_cec_data/$ins ]; then
    echo 'there is a dir for saving data'
else
    mkdir -p /vol/grid-solar/sgeusers/guanqiang/mpda_cec_data/$ins 
fi

cp -r /vol/grid-solar/sgeusers/guanqiang/mpda_ls_data/${ins}/ga_opt_${localSearch}_NORE /vol/grid-solar/sgeusers/guanqiang/mpda_cec_data/${ins}
# qsub mpda_scripts.sh ${ins} ${localSearch}
# bash ./local_mpda_scripts.sh ${ins} ${localSearch}
done
done
