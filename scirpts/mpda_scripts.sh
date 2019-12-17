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
echo ==Leon Test 3==
echo ==t==
# uname -n
# echo ==Leon Gao==
# id
# groups
# echo ==SGE_O_WORKDIR==
# echo $SGE_O_WORKDIR
# echo ==/LOCAL/TMP==
# ls -ltr /local/tmp/
# echo ==/VOL/GRID-SOLAR==
# ls -l /vol/grid-solar/sgeusers/
# 
# OK, where are we starting from and what's the environment we're in
# 
# echo ==RUN HOME==
# pwd
# ls
# echo ==ENV==
# env
# echo ==SET==
# set
# 
# echo == WHATS IN LOCAL/TMP ON THE MACHINE WE ARE RUNNING ON ==
# ls -ltra /local/tmp | tail
# 
# echo == WHATS IN LOCAL TMP guanqiang JOB_ID AT THE START==
# ls -la 
#
# Copy the input file to the local directory
#

# echo  dir ===$(pwd)====
pwd
cp  -r /vol/grid-solar/sgeusers/guanqiang/MPDAConf .
echo ==WHATS THERE HAVING COPIED STUFF OVER AS INPUT==
ls -a 
cd MPDAConf

echo 'instance ==========' $1
echo 'method ======== ' ga_opt_$2


if [ -d ./debugData/ga_opt_$2 ]; then
    echo 'there is a dir for saving data'
else
    mkdir -p ./debugData/ga_opt_$2 
fi


for rdSeed in $(seq 1 2 3)
do
   echo "run $rdSeed times"
#    python3  -W ingore run_alg.py   $1 $rdSeed $2
   python3  run_alg.py   $1 $rdSeed $2
    cp  ./debugData/$1/ga_opt_$2/*.dat ${DATA_PATH}/$1/ga_opt_$2/
done


DATA_PATH=/vol/grid-solar/sgeusers/guanqiang/mpda_exp_data/

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

