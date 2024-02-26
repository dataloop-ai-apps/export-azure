# Azure Hooks

The **Azure Hooks** application has two nodes to Export and Import annotation directly from Azure bucket.  \

## Quick Start:

1. Go to `Pipelines` and `Create new pipeline`.
2. Build a custom work flow that requires Export/Import annotations to/from Azure container
3. Define the bucket name in the node configuration panel. \
4. Start pipeline

Pre-requirements: The Azure-hooks service get integration_name parameter it can be one of both:
*  Secrete name that holds the azure connection string.
*  Name of predefined integration to Azure blob


## Node inputs and Outputs:

Both Azure-hooks nodes get the same item as input and output

## How it works:

### Export Annotations to Azure
When an item passes through the node, will export the annotations to a json file and upload it to the Azure bucket. \
The file will be uploaded to the following location: \
`<driver_path>/<item.dir>/<item.name>.json`

### Import Annotations from Azure
When an item passes through the node, will download the JSON annotations file from the Azure bucket and update the item with the new annotations. \
The file will be downloaded from the following location: \
`<driver_path>/<item.dir>/<item.name>.json`


## Node Configuration TBD:

<img src="assets/node_configration.png" height="480">

**Configuration**

- **Node Name:** Display name on the canvas.
- **Container Name:** The container name to export/import the annotations


## Contributions, Bugs and Issues - How to Contribute

We welcome anyone to help us improve this app.  
[Here's](CONTRIBUTING.md) a detailed instructions to help you open a bug or ask for a feature request.