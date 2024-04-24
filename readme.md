
# Recipe Manager API
### The easiest way to manage your recipes.

---
![GitHub watchers](https://img.shields.io/github/watchers/MarsTwelve/Recipe_Manager_API)
![GitHub Repo stars](https://img.shields.io/github/stars/MarsTwelve/Recipe_Manager_API)<br>
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/MarsTwelve/Recipe_Manager_API?style=flat-square&labelColor=2a3439)
![GitHub forks](https://img.shields.io/github/forks/MarsTwelve/Recipe_Manager_API?style=flat-square&labelColor=2a3439)

## Description
The Recipe Manager API is a small project developed using python, FastAPI and a MySQL
database, witch supports CRUD operations. The main objective is to create an easy way to
organize and store diverse types of recipes. Some of the future objectives are to implement
a frontend to enhance user experience, and also containerize and host this on a webservice such as
Amazon AWS or other cloud service, for better app performance.
<br />

---
<br />

## Endpoints
- Through the **post**`/recipe`, you are able to create new recipes, sending relevant recipe information, and the recipe ingredients


- Through the **get**`/recipe`,  you are able to request all recipes currently stored on the database


- Through the **get**`/recipe{_recipe_query_title_}`, you are able to search for specific recipes, by recipe title


- Through the **patch**`/recipe`, you are able to update the information about a specific recipe


- Through the **delete**`/recipe`, you are able to delete a specific recipe

---
<br />

## Installing and Running
- ### Setting up the database
    In order to run this pyton script, firstly you will need to install MySQL, this is due to the
    API currently only being able to be run locally. I also recommend installing DBeaver, if you wish
    to see and analyze the data you are working with.
<br />

  [MySQL for Linux](https://dev.mysql.com/downloads/)<br>
  [DBeaver for Linux](https://dbeaver.io/download/)<br>
<br />
<br />
<br />

### Installing the dependencies
After you installed MySQL you should run this command within your IDE terminal, to ensure the python libraries utilized
are properly installed.
<br />

```
pip install -r requirements.txt
```
<br />
<br />
<br />

### Initializing the API
After you ran the command above, you can now run this command to initialize the api.<br>
```
uvicorn endpoints.recipe_manager_API:app --reload
```
this will start the api in your local host, so you can utilize the api endpoints within your own machine, in a local instance.
Later on it is planned to implement a Cloud Service host with docker containers, in order to facilitate usage.
<br />
<br />
<br />

### Running tests
Within this script there pytest tests implemented. If you desire to run the test file to assert everything works
properly you can use this command to show the test results in a verbose manner.
```
pytest -v
```
