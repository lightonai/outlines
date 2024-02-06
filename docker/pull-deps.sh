#!/bin/bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi
REGION=us-west-2

CONTAINER_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/vllm:latest"

aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${ACCOUNT_ID}".dkr.ecr."${REGION}".amazonaws.com

docker pull $CONTAINER_URI

docker tag $CONTAINER_URI vllm
