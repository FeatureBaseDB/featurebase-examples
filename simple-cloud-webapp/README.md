</h1>
<p align="center">Create a simple project with FeatureBase Cloud and Anvil.works all in python! </p>

This example provides a ground-zero approach from no data or environment all the way to fully implemented local data generation, FeatureBase Cloud, and functioning web-app. All this solely with free online tools and a laptop. 

## ⚡️ Quick start

First, let's get the free Cloud accounts set-up and then we'll move to local environment tools. 

Navigate to the FeatureBase website and setup a free cloud trial [here](https://cloud.featurebase.com/signup).

Next do the same for a free Anvil.works account [here](https://anvil.works/).

Lastly, we'll be using Jupyter Notebook locally for a few steps and install steps can be found [here](https://jupyter.org/install).

  >For mac users you'll need a package manager to install both Python 3 and Jupyter (latest notebooks require Python 3). One option is [Homebrew](https://brew.sh/), and the following code helps with that method.
  > 
  > Install Latest Python 3
```bash
$ pyenv install 3.x.x
```
 > Install Jupyter using Homebrew 
 ```bash
$ brew install jupyter
```
 >Verify Jupyter Installation 
  ```bash
$ jupyter notebook
```
## 🚧  Database Setup & Data Generation

Once Jupyter is up and running, you can load [this](https://github.com/FeatureBaseDB/featurebase-examples/blob/main/simple-cloud-webapp/data-generation/jupyternotebook-example) code to create a pre-configured notebook with the modules needed. 


### Authenticate and Create FeatureDatabase

We will be using FeatureBase's HTTP API to interface from Jupyter Notebook using the *requests* library. For this you will need your username and password used to create your FeatureBase account. 

> If you are not using the Jupyter Notebook provided, you can find more resources to help with programmtic access to FeatureBase [here](https://docs.featurebase.com/setting-up-featurebase/cloud/programmaticaccess).

Frist we will need to update the information in the following cell:
- username
- password

Optional:
- database_name = The name given to a created database under the Featurebase Account (default: "customer_loyalty")
- deployment_shape = The available memory given to the created database (deafult is 8GB)
- table_name = The name of the table that is referenced (**used frequenlty** default: "seg")
- table_description = A quick description of the table contents
![Screen Shot 2022-10-19 at 2 15 28 PM](https://user-images.githubusercontent.com/75812579/196783421-602c482b-c57a-43b0-8e26-ef8505247e52.png)




