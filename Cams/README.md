# Mobile-Catlog
Udacity Full Stack Nano Degree Project 4

The fourthproject of the [Udacity Full Stack Web Developer Nanodegree Program](https://in.udacity.com/course/full-stack-web-developer-nanodegree--nd004) called "Build a Item-catlog".

## Project Overview

Your task is to create a Item-Catlog that show category Items and thier Information clearly.This Project need **Python, Flask frame work as Backend and HTML, CSS/Bootsrap as frontend**.

## Table Of Contents


- [Download](#download)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Documentation](#documentation)
- [Running Documents Locally](#running-documents-locally)
- [Output](#output)
- [References](#references)
- [Bug And Feature Requests](#bug-and-feature-requests)


## Download
The files for the project, [download](https://github.com/vijju3335/Mobile-Catlog/archive/master.zip).

### What's included

Within the download you'll find the following directories and files:

```
LogsAnalysis-master.zip/
|
└── Output
|     |
|     └── brandJSON.jpg
|     └── modelJSON.jpg
|     └── showBrandLog.jpg
|     └── showModelLog.jpg
|     └── showSpecLog.jpg
|     └── editSpecLog.jpg
|     └── ....
|
└── static
|     |
|     └── images
|     |      |
|     |      └── os.jpg
|     |      └── processor.jpg
|     |      └── sim.jpg
|     |      └── price.jpg
|     |      └── ram.jpg
|     |      └── storage.jpg
|     |      └── ....
|     └── css
|           └── main.css
|
└── templates
|     |
|     └── deleteBrand.html
|     └── deleteModel.html
|     └── editBrand.html
|     └── editModel.html
|     └── login.html
|     └── newBrand.html
|     └── newModel.html
|     └── showBrands4User.html
|     └── showModels4User.html
|     └── showSpecificationsOfModel.html
|
└── README.md
|
└── clients_secrets.json
|
└── database_setupMain.py
|
└── database_setupMain.pyc
|
└── final_project.py
|
└── mobileWorld.db
|
└── requirements.txt
```

## Software Requirements

This project should run in a **Virutalenv**, for that we use **Vagrant** to setup following modules from **PIP**.

- Python
- Pip
- SQLAlchemy
- Flask
- Virtualenv
- Requests
- Oauth2client

## Installation

To [Install](#install-requirements) above dependencies, use requiremnts.txt i.e contains commands to install all of them. These should be install in flask-env.
process goes here.
  #### Create Virtualenv
  ```
  virtualenv envName
  ```
  if any error occured, use this command ``` virtualenv --no-site-packages envName --always-copy ```
  
  #### Install Requirements
  use below command to install all dependencies ``` pip install -r requirements.txt ```
  
## Documentation

- downloaded zip file contains above mentioned files.
- **Output** constains screenshots of Project Sample output.
- **static** contains css files for styling **HTML** files.
- **templates** contains **HTML** files.These are used to render data from .py file.
- **client_secrets.json** contains oauth2clients project credentials details.
- **databaseSetupMain.py** contains classes to create Tables to DB.
- **final_project.py** contains flask frame scripting to route requests and response.
- **mobileWorld.db** is Database file.
- **requirements.txt** contains commands to install required dependencies.

- This Project is about Mobile Brands and their corresponding Models.**Brands** have properties like Name,Id,User_id. coming to **Models** have Name, Id, User_id, ....i.e see from database_setupMain.py files.
- Only Corresponding User can only Edit / Delete the Brand/Model.
- User must Login to Add New Brand/Model.
- No one Allowed to any Brand/Model wihour Permissions.

## Running Documents Locally

- To Run project, We use Vagrant Environment. For that we wants to Install **Vagrant** and **VirtualBox**.
- To install go [here](https://github.com/vijju3335/Vagrant-Installation).
- We made work easy by using python 2.7
- To Run this Catlog project in Web Browser From Vagrant, we must make port-forwarding.
- open Vagrantfile and add following lines of code.
  ```config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1" ```
- This is because, to use port 5000 in Host to Run project in web browser.
     #### Google Oauth
      Here we use Google Oauth v2 api to store User Data in Database.For this we need json file.we should follow simply few steps. 

      - Open [Google API Console](https://console.developers.google.con/)
      - Go to credentials, create new project by providing required information.
      - for example, see this [Image](https://github.com/vijju3335/Mobile-Catlog/blob/master/Output/jsonDemo.JPG)
      - Now download jsonfile and use in project.
  
  - To activate flask- ``` vagrant@vagrant:/vagrant/flaskEnv$ source flaskenv/bin/activate```
  flaskenv is my envName
  - To stop ,``` vagrant@vagrant:/vagrant/flaskEnv$ deactivate```
  -use this command to run project, by going to loaction of final_project.py file.
  ```
  (flask-env)vagrant@vagrant:/vagrant/flaskEnv/ItemCatlog$ python final_project.py
  ```
  
    #### JSON 
       - To get All Models of Particular Brand as JSON object
       ```localhost:5000/brand/brand_id/JSON```
       - To get  Particular Model details as JSON object
       ```localhost:5000/brand/brand_id/model/model_id/JSON```
## Output
  see Output from images in [Output file](https://github.com/vijju3335/Mobile-Catlog/blob/master/Output)
  
  - For better output use pictures of size more than 700X400.
  
## References

- stack overflow to errors retriving.
- sqlalchemy documentation [online](http://www.sqlalchemy.org/library.html#tutorials)

---

## Bug And Feature Requests
- Have a bug or a feature request? Please feel free to open an [issue](https://github.com/vijju3335/Mobile-Catlog/issues).



   
