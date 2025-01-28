from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

import dtlpy as dl
import logging
import base64
import json
import os

logger = logging.getLogger(name='Azure Export & Import')


class AzureExport(dl.BaseServiceRunner):
    def __init__(self):
        """
        Initializes the ServiceRunner with Azure Export & Import API credentials.
        """
        self.logger = logger
        self.logger.info('Initializing Azure Export & Import API client')
        raw_credentials = os.environ.get("AZURE_INTEGRATION", None)
        if raw_credentials is None:
            raise ValueError(f"Missing Azure integration.")

        try:
            decoded_credentials = base64.b64decode(raw_credentials).decode("utf-8")
            credentials = json.loads(decoded_credentials)
        except Exception:
            raise ValueError(f"Unable to decode the service integration. "
                             f"Please refer to the following guide for proper usage of Azure integrations with"
                             f"Dataloop: https://github.com/dataloop-ai-apps/export-azure/blob/main/README.md")

        client_secret_credential = ClientSecretCredential(
            tenant_id=credentials['tenantId'],
            client_id=credentials['clientId'],
            client_secret=credentials['secret']
        )
        # Create a BlobServiceClient using the Azure AD credential
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{credentials['key']}.blob.core.windows.net",
            credential=client_secret_credential
        )

    def export_annotation(self, item: dl.Item, context: dl.Context):
        if context is not None and context.node is not None and 'customNodeConfig' in context.node.metadata:
            container_name = context.node.metadata['customNodeConfig']['container_name']
            logger.info('Container name set to: {}'.format(container_name))
        else:
            raise ValueError("Node configration in context is missing, can't determinate the container name")

        annotation_json = item.to_json()
        annotation_json['annotations'] = item.annotations.list().to_json()['annotations']
        filename, _ = os.path.splitext(item.filename)
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(f"{filename[1:]}.json")
        blob_client.upload_blob(json.dumps(annotation_json), overwrite=True)
        return item

    def import_annotation(self, item: dl.Item, context: dl.Context):
        if context is not None and context.node is not None and 'customNodeConfig' in context.node.metadata:
            container_name = context.node.metadata['customNodeConfig']['container_name']
            logger.info('Container name set to: {}'.format(container_name))
        else:
            raise ValueError("Node configration in context is missing, can't determinate the container name")

        container_client = self.blob_service_client.get_container_client(container_name)
        filename, _ = os.path.splitext(item.filename)
        blob_client = container_client.get_blob_client(f"{filename[1:]}.json")
        blob_data = blob_client.download_blob().readall()
        data = json.loads(blob_data.decode('utf-8'))
        item.annotations.upload(annotations=data['annotations'])
        return item
