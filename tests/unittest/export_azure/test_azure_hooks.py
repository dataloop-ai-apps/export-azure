import os
import unittest
import dtlpy as dl

from modules.azure_hooks import AzureExport


class Node:
    def __init__(self, metadata):
        self.metadata = metadata


class TestRunner(unittest.TestCase):
    def setUp(self):
        item_id = ""
        container_name = ""
        remote_filepath = "/clones/1.jpg"

        # Connect .env file
        if os.environ.get("AZURE_API_KEY") is None:
            raise ValueError("Missing Azure service integration.")
        self.runner = AzureExport()
        self.original_item = dl.items.get(item_id=item_id)
        self.original_annotations = self.original_item.annotations.list()
        try:
            item = self.original_item.dataset.items.get(filepath=remote_filepath)
            item.delete()
        except dl.exceptions.NotFound:
            pass

        self.item = self.original_item.clone(remote_filepath=remote_filepath)
        self.context = dl.Context()
        self.context._node = Node(metadata={'customNodeConfig': {'container_name': container_name}})

    def test_export_annotations(self):
        self.runner.export_annotation(item=self.item, context=self.context)

    def test_import_annotations(self):
        self.item.annotations.delete(filters=dl.Filters(resource=dl.FiltersResource.ANNOTATION))
        self.runner.import_annotation(item=self.item, context=self.context)
        assert len(self.item.annotations.list()) == len(self.original_annotations)


if __name__ == "__main__":
    unittest.main()
