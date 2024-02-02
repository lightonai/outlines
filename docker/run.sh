docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 \
    --ipc=host \
    -e MODEL=mistralai/Mistral-7B-Instruct-v0.2 \
    outlines \
    --host 0.0.0.0 \
    --load-format safetensors

docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 \
    --ipc=host \
    -e MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1 \
    outlines \
    --tensor-parallel-size 4 \
    --host 0.0.0.0 \
    --load-format safetensors