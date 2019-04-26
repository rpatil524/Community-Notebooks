#!/usr/bin/env bash

#
# Set all the personal information in this file:
#

source ./setEnvVars.sh

#
# Stop the VM:
#

echo "Shutting down the server VM"
gcloud compute instances stop ${MACHINE_NAME} --zone ${ZONE} --project ${PROJECT}