#!/usr/bin/env bash
set -euo pipefail

# Edit these values or export them before running the script
SUBSCRIPTION_ID=${SUBSCRIPTION_ID:-"3c903801-0878-49d9-9d2c-3ed7f0e0ad1c"}
RESOURCE_GROUP=${RESOURCE_GROUP:-"RG_JIT02"}
WORKSPACE=${WORKSPACE:-"cpu-project"}
COMPUTE_NAME=${COMPUTE_NAME:-"dev-ci"}
ENV_NAME=${ENV_NAME:-"pipeline-env:1"}

echo "Using subscription: $SUBSCRIPTION_ID"
az account set --subscription "$SUBSCRIPTION_ID"

echo "Ensure workspace exists: $WORKSPACE (resource group: $RESOURCE_GROUP)"
az ml workspace show -w "$WORKSPACE" -g "$RESOURCE_GROUP"

echo "Register environment ($ENV_NAME) from environments/environment.yml"
az ml environment create --file environments/environment.yml --name "$ENV_NAME" -w "$WORKSPACE" -g "$RESOURCE_GROUP"

echo "Create compute instance ($COMPUTE_NAME) if it does not exist"
az ml compute create -n "$COMPUTE_NAME" --type computeinstance --size Standard_DS3_v2 -w "$WORKSPACE" -g "$RESOURCE_GROUP" || true

echo "Submitting pipeline_job.yaml to workspace $WORKSPACE"
az ml job create --file pipeline_job.yaml -w "$WORKSPACE" -g "$RESOURCE_GROUP"

echo "Submitted. Use 'az ml job stream --name <JOB_NAME> -w $WORKSPACE -g $RESOURCE_GROUP' to follow logs."
