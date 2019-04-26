#!/usr/bin/env bash

#
# Set all the personal information in this file:
#

source ./setEnvVars.sh

#
# Restart the VM:
#

echo "Starting up the server VM"
gcloud compute instances start ${MACHINE_NAME} --zone ${ZONE} --project ${PROJECT}