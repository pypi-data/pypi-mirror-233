from mlflow import MlflowClient
import yaml
import os
import mlflow

from flowi.prediction import flavors

_mlflow_client: MlflowClient = MlflowClient()


def map_model_flavor(model_flavor: str):
    if (
        model_flavor == "torch"
        or model_flavor == "pytorch_lightning"
        or model_flavor == "lightning"
    ):
        return "pytorch"
    elif model_flavor == "keras":
        return "tensorflow"

    return model_flavor


def _get_run_id_by_version(model_name: str, version: str):
    model_version_obj = _mlflow_client.get_model_version(model_name, version)
    return model_version_obj.run_id


def _get_flavor_from_model_info(model_info_path):
    with open(model_info_path) as file:
        model_info = yaml.safe_load(file)
    flavors_ = list(model_info["flavors"].keys())
    flavors_.remove("python_function")
    return flavors_[0]


def _get_model_flavor_from_mlflow(run_id: str, artifact_path: str):
    model_info_path = _mlflow_client.download_artifacts(
        run_id=run_id, path=os.path.join(artifact_path, "MLmodel"), dst_path=".."
    )
    model_flavor = _get_flavor_from_model_info(model_info_path=model_info_path)
    model_flavor = map_model_flavor(model_flavor=model_flavor)
    os.remove(model_info_path)

    return model_flavor


def get_model_flavor_module(model_flavor: str):
    model_flavor = map_model_flavor(model_flavor=model_flavor)

    # if model_flavor in get_custom_model_flavors():
    #     model_flavor_module = getattr(koopa.flavors, model_flavor + "_flavor")
    #     class_name = model_flavor.capitalize() + "Flavor"
    #     model_flavor_module = getattr(model_flavor_module, class_name)()
    # else:
    model_flavor_module = getattr(mlflow, model_flavor)

    return model_flavor_module


def load_model_by_version(
    model_name: str, version: str or int, artifact_path: str = "model"
):
    if not str(version).isnumeric():
        raise ValueError("Version must be a number")

    run_id = _get_run_id_by_version(model_name=model_name, version=version)
    model_flavor = _get_model_flavor_from_mlflow(
        run_id=run_id, artifact_path=artifact_path
    )

    model_flavor_module = get_model_flavor_module(model_flavor)
    model = model_flavor_module.load_model(model_uri=f"runs:/{run_id}/{artifact_path}")

    klass = getattr(flavors, model_flavor.capitalize() + "Flavor")

    return klass(model=model)


def _download_transformers_by_version(model_name: str, version: str):
    run_id = _get_run_id_by_version(model_name=model_name, version=version)
    _mlflow_client.download_artifacts(run_id=run_id, path="transformers/input_transformer.pkl",
                                      dst_path="input_transformer.pkl")
    _mlflow_client.download_artifacts(run_id=run_id, path="transformers/output_transformer.pkl",
                                      dst_path="output_transformer.pkl")


def _download_columns_by_version(model_name: str, version: str):
    run_id = _get_run_id_by_version(model_name=model_name, version=version)
    _mlflow_client.download_artifacts(run_id=run_id, path="columns.pkl", dst_path="columns.pkl")


def _download_drift_detector_by_version(model_name: str, version: str):
    run_id = _get_run_id_by_version(model_name=model_name, version=version)
    _mlflow_client.download_artifacts(run_id=run_id, path="drift_detector", dst_path="drift_detector")


def download_artifacts(model_name: str, version: str):
    _download_columns_by_version(model_name=model_name, version=version)
    _download_drift_detector_by_version(model_name=model_name, version=version)
    _download_transformers_by_version(model_name=model_name, version=version)

