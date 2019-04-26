#!/usr/bin/env bash

#
# Set all the personal information in this file:
#

source ./setEnvVars.sh

#
# Tear down the firewall rule:
#

echo "Deleting firewall rule"
gcloud compute firewall-rules delete ${FIREWALL_RULE_NAME} --project ${PROJECT}

#
# Release the static external IP:
#

echo "Releasing the static external IP"
gcloud compute addresses delete ${ADDRESS_NAME} --region ${REGION} --project ${PROJECT}
