FROM hub.dataloop.ai/dtlpy-runner-images/cpu:python3.10_opencv

# Install azure-storage-blob and azure-identity
RUN pip install azure-storage-blob azure-identity