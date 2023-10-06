"""
test_service.py

Generic test for services (training or prediction). Set up the service folder
(copy model code, download model artifact if necessary), install model
dependencies and set current working directory to service folder, then run:
python -m akerbp.mlops.services.test_service
"""
import json
import subprocess
import sys
import uuid
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Tuple, Union, Optional

from akerbp.mlops.cdf.helpers import get_client
from akerbp.mlops.core import config
from akerbp.mlops.core.helpers import subprocess_wrapper
from akerbp.mlops.core.logger import get_logger

service_name = config.ENV_VARS.service_name
platform = config.ENV_VARS.platform

logger = get_logger(__name__)

client_secrets = config.client_secrets


def mock_saver(*args, **kwargs):
    pass


def run_tests(test_path: Union[Path, str], path_type: str = "file") -> None:
    """
    Run tests with pytest. Raises exception subprocess.CalledProcessError
    if pytest fails.

    Input
      - test_path: path to tests with pytest (string or a list of strings) All
        should have the same format (see next parameter)
      - path_type: either 'file' (test_path refers then to files/folders) or
        'module' (test_path refers then to modules)

    """
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-s",
        "-o",
        "log_cli=true",
        "--color=no",
        "-W ignore:numpy.ufunc size changed",
    ]
    if path_type == "module":
        command.append("--pyargs")
    if isinstance(test_path, str) or isinstance(test_path, Path):
        command.append(str(test_path))
    elif isinstance(test_path, list):
        command += test_path
    else:
        raise ValueError("Input should be string or list of strings")
    logger.info(f"Run tests: {test_path}")
    subprocess_wrapper(command, stderr=subprocess.STDOUT)


def get_model_test_data(test_import_path: str) -> Tuple[Dict, Optional[Dict], bool]:
    """
    Read input and validation function from the model test file
    """

    service_test = import_module(test_import_path).ServiceTest()
    input = getattr(service_test, f"{service_name}_input")
    input_file_reference = getattr(
        service_test, f"{service_name}_input_file_reference", None
    )
    check = getattr(service_test, f"{service_name}_check")
    return input, input_file_reference, check  # type: ignore


def test_service(input: Dict, check: Any) -> None:
    """
    Generic service test. Call service with the model's test input data and
    validate the output.
    """
    logger.info(f"Test {service_name} service")
    service = import_module(f"akerbp.mlops.services.{service_name}").service

    if service_name == "training":
        response = service(data=input, secrets=client_secrets, saver=mock_saver)
    elif service_name == "prediction":
        response = service(data=input, secrets=client_secrets)
        # Check for predictions uploaded to CDF Files and delete to avoid unneccesary clogging
        if platform == "cdf" and response["prediction_file"] != "":
            import akerbp.mlops.cdf.helpers as mlops_helpers

            mlops_helpers.client_secrets = client_secrets
            mlops_helpers.set_up_cdf_client(context="write")
            cognite_client = mlops_helpers.global_client["write"]
            prediction_file_external_id = response["prediction_file"]
            logger.info(f"Deleting prediction file {prediction_file_external_id}")
            try:
                cognite_client.files.delete(external_id=prediction_file_external_id)
            except Exception as e:
                logger.warning(f"Error deleting prediction file: {e}")

    else:
        raise Exception("Unknown service name")

    assert response["status"] == "ok"


if __name__ == "__main__":
    logger = get_logger(name="akerbp.mlops.services.test_service.py")

    c = config.read_service_settings()
    run_tests(c.test_file)
    input, input_file_reference, check = get_model_test_data(c.test_import_path)
    test_service(input, check)
    if input_file_reference is not None:
        # Upload input to cdf files, and pass that ref
        client = get_client(
            client_id=client_secrets["id-write"],
            client_secret=client_secrets["secret-write"],
            tenant_id=client_secrets["tenant-id"],
            base_url=client_secrets["base-url"],
        )
        content_to_upload = str(json.dumps(input["input"][0]["input_logs"]))
        file_id = uuid.uuid4().hex
        external_file_id = f"mlops_test_service_input_{file_id}.binary"
        client.files.upload_bytes(
            content=content_to_upload,
            name=external_file_id.split(".")[0],
            external_id=external_file_id,
        )
        input_file_reference["input"][0]["input_file_reference"] = external_file_id
        test_service(input_file_reference, check)
        client.files.delete(external_id=external_file_id)
    # Share input with main process:
    print(json.dumps(input))
