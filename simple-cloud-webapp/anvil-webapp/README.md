# Building a Simple Web App on Anvil's Hosted Platform 

> In searching for an easy way to get started working on a Front-End, I came across Anvil and thought I would give it a shot. You can of course go a local route with Flask, but I chose to try to keep the data and development in the cloud after ingress. 
    
### Step 1    
#### Log in to Anvil and click ‘New Blank App’. 

![Screen Shot 2022-10-24 at 10 04 34 AM](https://user-images.githubusercontent.com/75812579/197559681-93d535c1-5d73-40d9-93f1-6eba832e4792.png)

### Step 2 
#### ON the *Design Tab* Drag and Drop Components onto the Blank App 
Example: [here](https://anvil.works/learn/tutorials/dashboard/chapter-1)
> In this design, we want to minimize latency and the necessity to do any pre-computation/pre-aggregation. Thus, I don't want to store query results in Anvil, I want FeatureBase to do the heavy crunching at runtime, allowing me to focus on handling results. You have the option to create a datagrid using Anvil's [uplink](https://anvil.works/learn/tutorials/external-database/chapter-2) functionality, however for this excercise I wanted to build out simple HTTP Requests and use buttons to get feel for querying an external database from Anvil. (Remember I'm a beginner on this!) 

