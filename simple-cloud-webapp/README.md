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


Next, we run the *Authentication* cell to request a token to use in future requests:
![Screen Shot 2022-10-19 at 2 30 12 PM](https://user-images.githubusercontent.com/75812579/196786075-afa3c531-a747-46ef-88ef-eea2d0b37b3e.png)


It's time to create the database we will load data into by running the *Create Database* cell:![Screen Shot 2022-10-19 at 2 32 01 PM](https://user-images.githubusercontent.com/75812579/196786406-1b46563d-8c20-450c-ac6f-ecd00a8a71e5.png)

### Create FeatureBase Table 

Once the database is created, we can make the Table we will be interacting with by running the *Create Table* cell: 
![Screen Shot 2022-10-19 at 2 33 58 PM](https://user-images.githubusercontent.com/75812579/196786748-e7942e11-57cb-4c04-ac92-adfb435b4627.png)

The final step is to create the columns we will be ingesting data into with the *Create Table Columns* cell:
![Screen Shot 2022-10-19 at 3 07 46 PM](https://user-images.githubusercontent.com/75812579/196793346-fa3bf1e4-ff5b-47a3-b935-d3c629a08254.png)

### Create Streaming Endpoint (Sink)

Now that a table is ready to receive data we need to create an endpoint in order to recieve our streaming data. To do this, run the *Create Sink* cell:
![Screen Shot 2022-10-19 at 3 11 47 PM](https://user-images.githubusercontent.com/75812579/196794066-5b27544a-2dcb-45d3-a345-1b5a184af1a7.png)

### Generate Data and Stream!

Finally, we can run the cell *Generate and Send Records* to create values for our table and stream them into our newly created Database & Table: 

![Screen Shot 2022-10-19 at 3 13 17 PM](https://user-images.githubusercontent.com/75812579/196794342-e3b12548-d990-4774-bd26-de255c74803c.png)







