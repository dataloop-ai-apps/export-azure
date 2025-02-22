# Azure Hooks

The **Azure Hooks** application has two nodes to Export and Import annotation directly from Azure bucket.


## Quick Start:

1. Go to `Pipelines` and `Create new pipeline`.
2. Build a custom work flow that requires Export/Import annotations to/from Azure container
3. Define the bucket name in the node configuration panel.
4. Start pipeline

Pre-requirements: The Azure-hooks service needs an integration of `AZURE_API_KEY` that can be one of both:
*  Secrete name that holds the azure connection string.
*  Name of predefined integration to Azure blob


## Node inputs and Outputs:

Both Azure-hooks 2 nodes get the same item as input and output


## How it works:

### Export Annotations to Azure
When an item passes through the node, the node will export the item annotations to a json file and upload it to the Azure bucket. \
The file will be uploaded to the following location: \
`<driver_path>/<item.dir>/<item.name>.json`

### Import Annotations from Azure
When an item passes through the node, the node will download the item JSON annotations file from the Azure bucket and update the item with the new annotations. \
The file will be downloaded from the following location: \
`<driver_path>/<item.dir>/<item.name>.json`


## Setting Up Your Azure Project

To use these nodes, you need an Azure project. Follow these steps to get started:

1. Create a [Client Secret](https://docs.dataloop.ai/docs/azure-datalake-gen2-1#:~:text=for%20the%20integration.-,Create%20a%20New%20Client%20Secret,-Once%20you%20create).
2. Create a [Storage Account](https://docs.dataloop.ai/docs/azure-datalake-gen2-1#:~:text=the%20Integration%20phase.-,Create%20a%20Storage%20Account,-Open%20Microsoft%20Azure).
3. Create a [Container](https://docs.dataloop.ai/docs/azure-datalake-gen2-1#:~:text=account%20in%20Azure.-,Create%20a%20Container,-Open%20Microsoft%20Azure).
4. Add [IAM Role Assignments](https://docs.dataloop.ai/docs/azure-datalake-gen2-1#:~:text=create%20a%20container.-,Add%20an%20IAM%20Role%20Assignments%20to%20a%20Container,-Select%20the%20chosen) 
   to the Container.


## Integrating Azure Export & Import API with Dataloop Platform

- Visit the [Dataloop Marketplace](https://docs.dataloop.ai/docs/marketplace), under Applications tab.
- Select the application and click on "Install" and then "Proceed".
  ![marketplace.png](assets/marketplace.png)
- Select an existing Azure integration or add a new one by creating an Azure integration with `key` and `secret`.
  ![add_integration.png](assets/add_integration.png)
- Install the application.
  ![add_integration_to_app.png](assets/add_integration_to_app.png)


## Node Configuration TBD:

<img src="assets/node_configration.png" height="480">

**Configuration**

- **Node Name:** The display name on the canvas.
- **Container Name:** The container name to export/import the annotations


## Contributions, Bugs and Issues - How to Contribute

We welcome anyone to help us improve this app.  
[Here's](CONTRIBUTING.md) a detailed instructions to help you open a bug or ask for a feature request.