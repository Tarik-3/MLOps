# Test pipeline (Azure ML)

This repo includes a test Azure ML pipeline that mounts an existing data asset, preprocesses, trains, evaluates, and runs a placeholder deploy step.

## Prerequisites
- Azure CLI logged in: `az login`
- Azure ML CLI extension: `az extension add -n ml -y`
- Python deps: `pip install -r requirements.txt`
- Access to subscription `3c903801-0878-49d9-9d2c-3ed7f0e0ad1c`, resource group `RG_JIT02`, workspace `cpu-project`.

## Data asset
- The pipeline reads Azure ML data asset `new_cpu_data` version `1` via the pipeline input in [test_pipeline_job.yaml](test_pipeline_job.yaml).

## Quick run (CLI)
```powershell
az ml job create --file test_pipeline_job.yaml -w cpu-project -g RG_JIT02
```

## Quick run (Python SDK)
```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_job

credential = DefaultAzureCredential()
ml_client = MLClient(
	credential=credential,
	subscription_id="3c903801-0878-49d9-9d2c-3ed7f0e0ad1c",
	resource_group_name="RG_JIT02",
	workspace_name="cpu-project",
)

pipeline = load_job("test_pipeline_job.yaml")
job = ml_client.jobs.create_or_update(pipeline)
print(job.name)
```

## Verify workspace and data access
```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
ml_client = MLClient(credential, "3c903801-0878-49d9-9d2c-3ed7f0e0ad1c", "RG_JIT02", "cpu-project")
ws = ml_client.workspaces.get("cpu-project")
print(ws.location, ":", ws.resource_group)
raw_data = ml_client.data.get(name="new_cpu_data", version="1")
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
