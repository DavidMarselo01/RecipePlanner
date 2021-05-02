## RecipePlanner

A recipe search site that also keeps a database of ingredients that a user currently has and allows users to search for all recipes that they can currently make with what is available. Created for CS-UY 4523 Design Project.

### Built With
* [Bootstrap](https://getbootstrap.com/)
* [Flask](https://flask.palletsprojects.com/)
* [MySQL](https://www.mysql.com/)

### Installation

1. Install Flask and MySQL

2. Clone the repo

3. Create a MySQL database named `RecipePlanner` (or whatever else you would want, provided that you set the name right during step 5)

4. Run the `Ingredients.sql`, `Recipes.sql`, and `TableDefinitionsRecipe.sql` scripts found in `/db` to populate the database's tables

5. Edit the Flask server settings on line 20 of `RecipePlanner.py` to match your MySQL database

6. Run `RecipePlanner.py` to start the server
