FROM vllm

# Install git
RUN apt-get update && apt-get install -y git

WORKDIR /workspace

COPY requirements.txt ./requirements-outlines.txt

RUN python3 -m pip install -U pip && python3 -m pip install -r requirements-outlines.txt

COPY outlines outlines

# Start the server
RUN chmod +x outlines/entrypoint.sh
ENTRYPOINT ["outlines/entrypoint.sh"]
