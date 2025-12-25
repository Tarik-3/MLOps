param(
    [string]$resourceGroup = "RG_JIT02",
    [string]$workspace = "cpu-project",
    [string]$subscriptionId = "3c903801-0878-49d9-9d2c-3ed7f0e0ad1c",
    [string]$computeName = "dev-ci",
    [string]$envName = "pipeline-env:1"
)

Write-Host "Setting subscription to $subscriptionId"
az account set --subscription $subscriptionId

Write-Host "Ensure workspace exists"
az ml workspace show -w $workspace -g $resourceGroup

Write-Host "Register environment ($envName)"
az ml environment create --file environments/environment.yml --name $envName -w $workspace -g $resourceGroup

Write-Host "Create compute instance ($computeName) if it does not exist"
az ml compute create -n $computeName --type computeinstance --size Standard_DS3_v2 -w $workspace -g $resourceGroup

Write-Host "Submitting pipeline_job.yaml to workspace $workspace"
az ml job create --file pipeline_job.yaml -w $workspace -g $resourceGroup

Write-Host "Done. Use 'az ml job stream --name <JOB_NAME>' to follow logs."
