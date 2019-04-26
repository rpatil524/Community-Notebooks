#!/usr/bin/env bash

#
# Set all the personal information in this file:
#

source ./setEnvVars.sh

#
# Delete the VM:
#

echo "Deleting the server VM"
gcloud compute instances delete ${MACHINE_NAME} --zone ${ZONE} --project ${PROJECT}
