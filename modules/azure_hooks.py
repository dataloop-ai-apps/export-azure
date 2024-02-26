from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

import dtlpy as dl
import logging
import base64
import json
import os

logger = logging.getLogger(name='Azure Export & Import')


class AzureExport(dl.BaseServiceRunner):
    def __init__(self, integration_name):
        connection_string = os.environ.get(integration_name.replace('-', '_'))

        integration_info = base64.b64decode(connection_string).decode("utf-8")
        integration_info = json.loads(integration_info)
        credential = ClientSecretCredential(
            tenant_id=integration_info['tenantId'],
            client_id=integration_info['clientId'],
            client_secret=integration_info['secret']
        )
        # Create a BlobServiceClient using the Azure AD credential
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{integration_info['key']}.blob.core.windows.net",
            credential=credential
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


def test():
    class Node:
        def __init__(self, metadata):
            self.metadata = metadata

    service_runner = AzureExport(integration_name="<integration name>")
    original_item = dl.items.get(item_id='')
    original_annotations = original_item.annotations.list()
    remote_filepath = "/clones/1.jpg"
    try:
        item = original_item.dataset.items.get(filepath=remote_filepath)
        item.delete()
    except dl.exceptions.NotFound:
        pass

    item = original_item.clone(remote_filepath=remote_filepath)
    context = dl.Context()
    context._node = Node(metadata={'customNodeConfig': {'container_name': ''}})
    service_runner.export_annotation(item=item, context=context)
    item.annotations.delete(filters=dl.Filters(resource=dl.FiltersResource.ANNOTATION))
    service_runner.import_annotation(item=item, context=context)
    assert len(item.annotations.list()) == len(original_annotations)


if __name__ == '__main__':
    test()
