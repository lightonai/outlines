# Deploy a model to SageMaker

## Install dependencies

```bash
pip install -r requirements-utils.txt
```

## Deploy a model

Deploy a model to SageMaker:

```bash
python utils/deploy.py --config_path utils/configs/mistral.json
```

> You can create more models configs in the `utils/configs` folder.

To clean up the SageMaker resources:

```bash
python utils/cleanup.py --endpoint_name <endpoint_name>
```
