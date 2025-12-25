import os
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, dsl, Input, Output, load_component

# Load command components from YAML definitions
# Paths are relative to repo root when running from project root
_data_prep = load_component(source="./components/preprocess/component.yaml")
_train = load_component(source="./components/train/component.yaml")
_evaluate = load_component(source="./components/evaluate/component.yaml")
_deploy = load_component(source="./components/deploy/component.yaml")


def get_ml_client() -> MLClient:
    """Create MLClient using DefaultAzureCredential and env variables."""
    subscription_id = os.environ["SUBSCRIPTION_ID"]
    resource_group = os.environ["RESOURCE_GROUP"]
    workspace = os.environ["WORKSPACE"]
    credential = DefaultAzureCredential()
    return MLClient(credential, subscription_id, resource_group, workspace)


# Define the DSL pipeline
def build_pipeline():
    @dsl.pipeline(
        compute="serverless",  # runs on serverless pipeline compute
        description="Test pipeline: preprocess -> train -> evaluate -> deploy",
    )
    def pipeline(
        data_asset: Input(type="uri_folder"),
        test_train_ratio: float = 0.2,
        learning_rate: float = 0.01,
        registered_model_name: str = "test-model",
    ) -> dict:
        preprocess_job = _data_prep(raw_data=data_asset)

        train_job = _train(
            train_data=preprocess_job.outputs.processed_data,
        )

        eval_job = _evaluate(
            model=train_job.outputs.model,
            test_data=preprocess_job.outputs.test_data,
        )

        deploy_job = _deploy(model=train_job.outputs.model)

        return {
            "train_data": preprocess_job.outputs.processed_data,
            "test_data": preprocess_job.outputs.test_data,
            "model": train_job.outputs.model,
            "metrics": train_job.outputs.metrics,
            "eval_report": eval_job.outputs.eval_report,
            "deploy_marker": deploy_job.outputs.get("marker", None),
        }

    return pipeline


def submit_pipeline():
    """Submit the DSL pipeline using environment variables for config."""
    ml_client = get_ml_client()
    pipeline_func = build_pipeline()

    data_asset_name = os.environ.get("DATA_ASSET", "new_cpu_data")
    data_asset_version = os.environ.get("DATA_VERSION", "1")

    pipeline_job = pipeline_func(
        data_asset=Input(type="uri_folder", path=f"azureml:{data_asset_name}:{data_asset_version}"),
    )

    returned_job = ml_client.jobs.create_or_update(pipeline_job)
    print(f"Submitted job: {returned_job.name}")


if __name__ == "__main__":
    submit_pipeline()
