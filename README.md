# Outlines

This repo is a fork of the [Outlines](https://github.com/outlines-dev/outlines) repo.

It contains the following changes:
- Deployment on SageMaker
- OpenAI API support for guided generation

## Deploy a model to SageMaker

To deploy a model to SageMaker using this image, follow the guide in [DEPLOY.md](DEPLOY.md).

## Contributing

### Pull the dependency image from ECR

The [`lightonai/vllm`](https://github.com/lightonai/vllm) image is a dependency of the outlines image. You need it for development and production build.

This command will pull the `lightonai/vllm` image from ECR.

```bash
sh docker/pull-deps.sh
```

### Build the image

To build the production image:

```bash
sh docker/build.sh
```

### Deploy the image to ECR

```bash
sh docker/deploy.sh
```

### Run the image locally

For Mistral:

```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 \
    --ipc=host \
    -e SERVED_MODEL_NAME=mistral \
    -e MODEL=mistralai/Mistral-7B-Instruct-v0.2 \
    outlines \
    --host 0.0.0.0 \
    --load-format safetensors
```

For Mixtral:
    
```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 \
    --ipc=host \
    -e SERVED_MODEL_NAME=mixtral \
    -e MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1 \
    outlines \
    --tensor-parallel-size 4 \
    --host 0.0.0.0 \
    --load-format safetensors
```

For Alfred:
    
```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 \
    --ipc=host \
    -e SERVED_MODEL_NAME=alfred \
    -e MODEL=lightonai/alfred-40b-1023 \
    outlines \
    --tensor-parallel-size 4 \
    --host 0.0.0.0 \
    --trust-remote-code
```

## Upgrade version

You can upgrade the version of outlines by rebasing on the official repo:

```bash
git clone https://github.com/lightonai/outlines
git remote add official https://github.com/outlines-dev/outlines
git fetch official
git rebase official/main
git rebase --continue # After resolving conflicts (if any), continue the rebase
git push origin main --force
```
