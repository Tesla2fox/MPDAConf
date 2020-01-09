#!/bin/sh
#
# Force Bourne Shell if not Sun Grid Engine default shell (you never know!)
#
#$ -S /bin/sh
#
# I know I have a directory here so I'll use it as my initial working directory
#
#$ -wd /vol/grid-solar/sgeusers/guanqiang 
#
# End of the setup directives
#
# Now let's do something useful, but first change into the job-specific
# directory that should have been created for us
#
# Check we have somewhere to work now and if we don't, exit nicely.
#
if [ -d /local/tmp/guanqiang/$JOB_ID ]; then
        cd /local/tmp/guanqiang/$JOB_ID
else
        echo "Uh oh ! There's no job directory to change into "
        echo "Something is broken. I should inform the programmers"
        echo "Save some information that may be of use to them"
        echo "Here's LOCAL TMP "
        ls -la /local/tmp
        echo "AND LOCAL TMP guanqiang "
        ls -la /local/tmp/guanqiang
        echo "Exiting"
        exit 1
fi
#
# Now we are in the job-specific directory so now can do something useful
#
# Stdout from programs and shell echos will go into the file
#    scriptname.o$JOB_ID
#  so we'll put a few things in there to help us see what went on
#
echo ==Leon MPDA Conf==
echo ==t==
pwd
cp  -r /vol/grid-solar/sgeusers/guanqiang/MPDAConf .
echo ==WHATS THERE HAVING COPIED STUFF OVER AS INPUT==
ls -a 
cd MPDAConf

echo 'instance ==========' $1
# echo 'method ======== ' ga_opt_$2



if [-d ./debugData/$1/eda_opt_]; then
    echo 'there is a dir for saving data'
else
    mkdir -p ./debugData/$1/eda_opt_ 
    echo 'create ./debugData/'$1'/ga_opt_'
fi

DATA_PATH=/vol/grid-solar/sgeusers/guanqiang/mpda_cec_data/

if [ -d ${DATA_PATH}/$1/eda_opt_ ]; then
    echo 'there is a dir for saving data'
else
    mkdir -p ${DATA_PATH}/$1/eda_opt_
fi

for rdSeed in $(seq 1 2 60)
do
   echo "rdSeed =  $rdSeed "
#    python3  -W ingore run_alg.py   $1 $rdSeed $2
   python3  run_eda.py  $1 $rdSeed 
    cp  ./debugData/$1/eda_opt_/*.dat ${DATA_PATH}/$1/eda_opt_/
done
done 
# for reStart in  _REGEN


# for rdSeed in $(seq 1 2 60)
# do
#    echo "run $rdSeed times"
#    python3  -w ingore run_alg.py   8_8_ECCENTRIC_RANDOM_UNITARY_QUADRANT_thre0.1MPDAins $rdSeed _SWAP
# done
# mkdir -p /vol/grid-solar/sgeusers/guanqiang/mpda_$JOB_ID

# cp -r ./debugData/ga_opt_$2  ${DATA_PATH}

# 
# Note that we need the full path to this utility, as it is not on the PATH
#
# /usr/pkg/bin/convert krb_tkt_flow.JPG krb_tkt_flow.png
#
# echo ==AND NOW, HAVING DONE SOMTHING USEFUL AND CREATED SOME OUTPUT==
# ls -la
#
# Now we move the output to a place to pick it up from later
#  (really should check that directory exists too, but this is just a test)
#
# cp krb_tkt_flow.png  /vol/grid-solar/sgeusers/guanqiang/$JOB_ID
#
echo "Ran through OK"

