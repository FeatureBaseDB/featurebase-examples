# Building a Simple Web App on Anvil's Hosted Platform 

> In searching for an easy way to get started working on a Front-End, I came across Anvil and thought I would give it a shot. You can of course go a local route with Flask, but I chose to try to keep the data and development in the cloud after ingress. 
    
### Step 1    
#### Log in to Anvil and click ‘New Blank App’. 

![Screen Shot 2022-10-24 at 10 04 34 AM](https://user-images.githubusercontent.com/75812579/197559681-93d535c1-5d73-40d9-93f1-6eba832e4792.png)

### Step 2 
#### ON the *Design Tab* Drag and Drop A Component onto the Blank App and label it using the text field 
Example: [here](https://anvil.works/learn/tutorials/dashboard/chapter-1)
> In this design, we want to minimize latency and the necessity to do any pre-computation/pre-aggregation. Thus, I don't want to store query results in Anvil, I want FeatureBase to do the heavy crunching at runtime, allowing me to focus on handling results. You have the option to create a datagrid using Anvil's [uplink](https://anvil.works/learn/tutorials/external-database/chapter-2) functionality, however for this excercise I wanted to build out simple HTTP Requests and use buttons to get feel for querying an external database from Anvil. (Remember I'm a beginner on this!) 

### Step 3 
#### Back on the Design Tab, go to Toolbox and Add a Card Component from under the Theme Elements
![Screen Shot 2022-10-24 at 10 40 25 AM](https://user-images.githubusercontent.com/75812579/197567594-befbd1c4-6f1a-476c-95fb-1585869cf8cf.png)


### Step 4 
# Drag and drop a Plot component from the toolboox into the Card layout 
![Screen Shot 2022-10-31 at 10 47 02 AM](https://user-images.githubusercontent.com/75812579/199049965-7ee61d08-7ddf-4976-b3ce-c02903917959.png)



### Step 5 
#### Setup a query to populate the Plot and then we can add some user interactivity 

 ```python
 
import anvil.http
import json
from .FB_Auth import featurebase_authenticate

```
