# Azure ML pipeline — quick start

This repository contains a minimal Azure ML Pipeline scaffold that runs on an Azure ML Compute Instance.

Overview
- Components: small `command` components under `components/` that run the scripts in `src/`.
- Environment: `environments/environment.yml` (registered by the submit script as `pipeline-env:1`).
- Pipeline definition: `pipeline_job.yaml` wired to run on compute `dev-ci`.
- Submit script: `submit_pipeline.ps1` registers the environment, creates the compute instance, and submits the job.

Prerequisites
- Azure CLI installed and logged in: `az login`
- Azure ML extension for CLI: `az extension add -n ml -y`
- You have access to the subscription, resource group, and workspace shown in the Azure portal screenshot.

Repository layout (key files)
- `pipeline_job.yaml` — pipeline graph and compute target per job
- `components/*/component.yaml` — component definitions
- `environments/environment.yml` — conda/pip spec used by components
- `src/*.py` — implementation for each component
- `submit_pipeline.ps1` — helper script to register the environment, create compute, submit the pipeline

Configured defaults (already filled)
- Subscription ID: ``
- Resource Group: ``
- Workspace: ``
- Compute name: ``
- Registered environment name: `pipeline-env:1`

How to submit the pipeline (one-shot)
1. Open PowerShell in the project root.
2. (Optional) Edit `submit_pipeline.ps1` to change `computeName` or `envName` if you prefer different names.
3. Run the script (it will register the environment, ensure compute exists, and submit the pipeline):

```powershell
.\submit_pipeline.ps1
```

What the script runs
- `az ml environment create --file environments/environment.yml --name pipeline-env:1`
- `az ml compute create -n dev-ci --type computeinstance --size Standard_DS3_v2`
- `az ml job create --file pipeline_job.yaml`

If you prefer to submit manually (CLI)
1. Register environment:
```powershell
az ml environment create --file environments/environment.yml --name pipeline-env:1 -w cpu-project -g RG_JIT02
```
2. Create compute (only once):
```powershell
az ml compute create -n dev-ci --type computeinstance --size Standard_DS3_v2 -w cpu-project -g RG_JIT02
```
3. Submit pipeline:
```powershell
az ml job create --file pipeline_job.yaml -w cpu-project -g RG_JIT02
```

Linux / WSL instructions
1. Open a Linux shell (native Linux or WSL) in the project root.
2. Make the Bash submit script executable:

```bash
chmod +x ./submit_pipeline.sh
```

3. Run the script (it uses the subscription/workspace values already configured):

```bash
./submit_pipeline.sh
```

4. To override defaults you can export environment variables before running:

```bash
export SUBSCRIPTION_ID=3c903801-0878-49d9-9d2c-3ed7f0e0ad1c
export RESOURCE_GROUP=RG_JIT02
export WORKSPACE=cpu-project
export COMPUTE_NAME=dev-ci
export ENV_NAME=pipeline-env:1
./submit_pipeline.sh
```

Notes about WSL
- If you use WSL, ensure Azure CLI is installed in WSL or run the script from Windows PowerShell (both approaches work). If you install Azure CLI in WSL, also install the `ml` extension: `az extension add -n ml -y`.


Alternative: submit via Python SDK
```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_job

cred = DefaultAzureCredential()
ml_client = MLClient(cred, "3c903801-0878-49d9-9d2c-3ed7f0e0ad1c", "RG_JIT02", "cpu-project")
pipeline = load_job(path="pipeline_job.yaml")
job = ml_client.jobs.create_or_update(pipeline)
print(job.name)
```

Monitoring and logs
- Show job status:
```powershell
az ml job show --name <JOB_NAME> -w cpu-project -g RG_JIT02
```
- Stream logs:
```powershell
az ml job stream --name <JOB_NAME> -w cpu-project -g RG_JIT02
```
- Use Azure ML Studio (studio.azureml) -> Select your workspace -> Experiments to inspect runs, download artifacts, and view metrics.

Notes & tips
- `pipeline_job.yaml` is already configured to use `compute: dev-ci` for each job. If you create a different compute name, either update the file or pass the desired compute in the script.
- The script registers the environment as `pipeline-env:1`. If you already have an environment with that name, the CLI will error; change `envName` in `submit_pipeline.ps1` or delete the existing environment before running.
- Artifacts (models, metrics, reports) produced by components are stored as job outputs and visible in the job details in Studio.
- For production workloads consider using a `ComputeCluster` for training jobs and enabling model registration and automated deployments.

Cleanup
To remove the compute instance (if created by the script):
```powershell
az ml compute delete -n dev-ci -y -w cpu-project -g RG_JIT02
```

Troubleshooting
- If submission fails, run `az ml job create --file pipeline_job.yaml` with `--debug` to see detailed errors.
- Use `az ml job download --name <JOB_NAME> --output ./artifacts` to fetch outputs locally for inspection.

Questions or changes
If you want, I can: update compute size, change the environment name, or add a step to automatically register the model after training. Tell me which.
