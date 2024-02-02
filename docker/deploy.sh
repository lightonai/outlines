#!/bin/bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]
then
    exit 255
fi
REGION=us-west-2

CONTAINER_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/outlines:latest"

aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${ACCOUNT_ID}".dkr.ecr."${REGION}".amazonaws.com
aws ecr describe-repositories --repository-names "outlines" --region "${REGION}" > /dev/null 2>&1
if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "outlines" --region "${REGION}" > /dev/null
fi


if docker build . --tag outlines
then
    docker tag outlines "$CONTAINER_URI"
    docker push "$CONTAINER_URI"
fi
