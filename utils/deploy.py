import re
import boto3
import fire
import random
import string
import json


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def get_sagemaker_vars(region, base_image_name):
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    return (
        f"{account_id}.dkr.ecr.{region}.amazonaws.com/{base_image_name}:latest",
        f"arn:aws:iam::{account_id}:role/SMRole",
    )


def print_color(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }
    print(colors[color] + text + "\033[0m")


def read_json_file(config_path: str):
    with open(config_path, "r") as file:
        data = json.load(file)
    return data


def get_value(config_data, cli_value, key):
    """
    Get the value from the CLI if it exists, otherwise use the config value.
    """
    if cli_value is not None:
        print_color(f"Using {key} from CLI: {cli_value}", "blue")
        return cli_value
    elif config_data is not None:
        print_color(f"Using {key} from config: {config_data.get(key, None)}", "yellow")
        return config_data.get(key, None)
    else:
        return None


def deploy(
    config_path: str,
    model: str = None,
    endpoint_name: str = None,
    image: str = None,
    instance_type: str = None,
    pipeline_parallel_size: int = None,
    tensor_parallel_size: int = None,
    max_model_len: int = None,
    region: str = "us-west-2",
):
    """
    Deploy a VLLM model to SageMaker.

    Args:
        model: The model name to deploy (i.e. `mistralai/Mistral-7B-Instruct-v0.2`).
        name: The name of the endpoint.
        region: The AWS region to deploy to.
        instance_type: The instance type to deploy to.
        base_image_name: The base image name to use.
    """
    config_data = read_json_file(config_path)
    model = get_value(config_data, model, "model")
    image = get_value(config_data, image, "image")
    instance_type = get_value(config_data, instance_type, "sagemaker_instance_type")
    pipeline_parallel_size = get_value(
        config_data, pipeline_parallel_size, "pipeline_parallel_size"
    )
    tensor_parallel_size = get_value(
        config_data, tensor_parallel_size, "tensor_parallel_size"
    )
    max_model_len = get_value(config_data, max_model_len, "max_model_len")

    random_id = generate_random_string(5)
    name = model.split("/")[-1] if endpoint_name is None else endpoint_name
    endpoint_name = "vllm-" + re.sub("[^0-9a-zA-Z]", "-", name) + "-" + random_id
    model_name = f"{endpoint_name}-mdl"
    endpoint_config_name = f"{endpoint_name}-epc"

    # get sagemaker image and role
    vllm_image_uri, role = get_sagemaker_vars(region, image)

    assert model is not None
    assert pipeline_parallel_size is not None
    assert tensor_parallel_size is not None

    container_env = {
        "MODEL": model,
        "PIPELINE_PARALLEL_SIZE": str(pipeline_parallel_size),
        "TENSOR_PARALLEL_SIZE": str(tensor_parallel_size),
        "SERVED_MODEL_NAME": endpoint_name,
    }

    if max_model_len is not None:
        container_env["MAX_MODEL_LEN"] = str(max_model_len)

    print("\nThis configuration will be applied: ")
    print_color(
        json.dumps(
            {
                "container_env": container_env,
                "instance_type": instance_type,
                "sagemaker_endpoint": endpoint_name,
                "sagemaker_model": model_name,
                "sagemaker_endpoint_config": endpoint_config_name,
                "region": region,
                "image_uri": vllm_image_uri,
            },
            indent=4,
        ),
        "green",
    )

    # create model
    sm_client = boto3.client(service_name="sagemaker", region_name=region)
    create_model_response = sm_client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=role,
        PrimaryContainer={"Image": vllm_image_uri, "Environment": container_env},
    )
    print("Model Arn: " + create_model_response["ModelArn"])

    # create endpoint configuration
    create_endpoint_config_response = sm_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "InstanceType": instance_type,
                "InitialVariantWeight": 1,
                "InitialInstanceCount": 1,
                "ModelName": model_name,
                "VariantName": "AllTraffic",
            }
        ],
    )
    print(
        "Endpoint Config Arn: " + create_endpoint_config_response["EndpointConfigArn"]
    )

    # create endpoint
    create_endpoint_response = sm_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name,
    )

    print(f"Waiting for {endpoint_name} endpoint to be in service...")
    waiter = sm_client.get_waiter("endpoint_in_service")
    waiter.wait(EndpointName=endpoint_name)

    resp = sm_client.describe_endpoint(EndpointName=endpoint_name)
    print("Endpoint Arn: " + create_endpoint_response["EndpointArn"])
    print("Endpoint Status: " + resp["EndpointStatus"])
    print("=" * 20)
    print("Endpoint name: " + endpoint_name)
    print("=" * 20)

    return endpoint_name


if __name__ == "__main__":
    fire.Fire(deploy)
