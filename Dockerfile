FROM dataloopai/dtlpy-agent:cpu.py3.10.opencv

# Install azure-storage-blob and azure-identity
RUN pip install azure-storage-blob azure-identity