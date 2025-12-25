# Test pipeline (Azure ML)

This repo includes a test Azure ML pipeline that mounts an existing data asset, preprocesses, trains, evaluates, and runs a placeholder deploy step.

## Prerequisites
- Azure CLI logged in: `az login`
- Azure ML CLI extension: `az extension add -n ml -y`
- Python deps: `pip install -r requirements.txt`
- Set your workspace context via environment variables (example):
	- PowerShell:
		```powershell
		$env:SUBSCRIPTION_ID="<your-subscription-id>"
		$env:RESOURCE_GROUP="<your-resource-group>"
		$env:WORKSPACE="<your-workspace-name>"
		$env:DATA_ASSET="new_cpu_data"
		$env:DATA_VERSION="1"
		```
	- Bash:
		```bash
		export SUBSCRIPTION_ID="<your-subscription-id>"
		export RESOURCE_GROUP="<your-resource-group>"
		export WORKSPACE="<your-workspace-name>"
		export DATA_ASSET="new_cpu_data"
		export DATA_VERSION="1"
		```

## Data asset
- The pipeline reads Azure ML data asset `new_cpu_data` version `1` via the pipeline input in [test_pipeline_job.yaml](test_pipeline_job.yaml).

## Quick run (CLI)
```powershell
az ml job create --file test_pipeline_job.yaml -w $env:WORKSPACE -g $env:RESOURCE_GROUP
```

## Quick run (Python SDK)
```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_job

credential = DefaultAzureCredential()
ml_client = MLClient(
	credential=credential,
	subscription_id=os.environ["SUBSCRIPTION_ID"],
	resource_group_name=os.environ["RESOURCE_GROUP"],
	workspace_name=os.environ["WORKSPACE"],
)

pipeline = load_job("test_pipeline_job.yaml")
job = ml_client.jobs.create_or_update(pipeline)
print(job.name)
```

## Run via DSL (Python-only, no CLI)
Use environment variables for your workspace and data asset, then run the DSL script:

PowerShell example:
```powershell
$env:SUBSCRIPTION_ID="<your-subscription-id>"
$env:RESOURCE_GROUP="<your-resource-group>"
$env:WORKSPACE="<your-workspace-name>"
$env:DATA_ASSET="new_cpu_data"
$env:DATA_VERSION="1"
python .\src\pipeline_dsl.py
```

Bash example:
```bash
export SUBSCRIPTION_ID="<your-subscription-id>"
export RESOURCE_GROUP="<your-resource-group>"
export WORKSPACE="<your-workspace-name>"
export DATA_ASSET="new_cpu_data"
export DATA_VERSION="1"
python ./src/pipeline_dsl.py
```

The DSL pipeline uses `serverless` compute and stitches the existing YAML command components: preprocess → train → evaluate → deploy.

## Verify workspace and data access
```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
ml_client = MLClient(
	credential=credential,
	subscription_id=os.environ["SUBSCRIPTION_ID"],
	resource_group_name=os.environ["RESOURCE_GROUP"],
	workspace_name=os.environ["WORKSPACE"],
)
ws = ml_client.workspaces.get(os.environ["WORKSPACE"])
print(ws.location, ":", ws.resource_group)
raw_data = ml_client.data.get(name=os.environ.get("DATA_ASSET", "new_cpu_data"), version=os.environ.get("DATA_VERSION", "1"))
print(f"Data asset URI: {raw_data.path}")
```

## Pipeline graph
- Preprocess: splits train/test ([components/preprocess/component.yaml](components/preprocess/component.yaml)).
- Train: produces model and metrics ([components/train/component.yaml](components/train/component.yaml)).
- Evaluate: scores model on test split ([components/evaluate/component.yaml](components/evaluate/component.yaml)).
- Deploy: placeholder marker ([components/deploy/component.yaml](components/deploy/component.yaml)).

## Environment
- Conda spec: [environments/environment.yml](environments/environment.yml)
- Includes `azure-ai-ml` and `azure-identity` for `DefaultAzureCredential`.

## Notes
- Compute target in the test pipeline is `dev-ci`. Update `compute` in [test_pipeline_job.yaml](test_pipeline_job.yaml) if you use a different name.
- The deploy step is a stub; replace [src/deploy.py](src/deploy.py) with real endpoint creation when ready.
