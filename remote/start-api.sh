#!/bin/bash

workspace=/homes/$USER
server_port=5000
virtualenv=/vol/bitbucket/$USER/msc
# Parse any options
while getopts "gw:p:s:" opt
do
    case "${opt}" in
        p) port=${OPTARG};;
        s) server_port=${OPTARG};;
    esac
done


# Interactive case with Jupyter Lab
LABM=`/vol/linux/bin/check_job.sh`
if [ $LABM == "1" ]; then
    echo "Error detected, no running job on GPU Cluster";
    echo "Submit GPU job at gpucluster2.doc.ic.ac.uk or gpucluster3.doc.ic.ac.uk"; echo "Quitting"
else
    echo "Job found, Connecting to $LABM.doc.ic.ac.uk"
    ssh -q -oUserKnownHostsFile=/dev/null -oBatchMode=yes -o StrictHostKeyChecking=no \
    -L $port:localhost:$port \
    -L $server_port:localhost:$server_port \
    -t ${LABM}.doc.ic.ac.uk "/vol/bitbucket/nuric/bin/runjupyter -w $workspace -p $port -e $virtualenv"
fi
