CREATE TABLE Person (
        username VARCHAR(32),
        password VARCHAR(64),
        firstName VARCHAR(32),
        lastName VARCHAR(32),
        email VARCHAR(32),
        PRIMARY KEY (username)
);

CREATE TABLE Recipes (
        recipe_name VARCHAR(32),
        instructions VARCHAR(3000),
        cook_time INT,
        PRIMARY KEY (recipe_name)
);

CREATE TABLE tag (
        tag_name VARCHAR(32),
        recipe_name VARCHAR(32),
        PRIMARY KEY (tag_name, recipe_name),
        FOREIGN KEY (recipe_name) REFERENCES Recipes (recipe_name)
);

CREATE TABLE Ingredients (
        ingredient_name VARCHAR(32),
        measure_unit VARCHAR(32),
        PRIMARY KEY (ingredient_name)
);

CREATE TABLE Aliasingredients (
        alias VARCHAR(32),
        ingredient_name VARCHAR(32),
        PRIMARY KEY (alias),
        FOREIGN KEY (ingredient_name) REFERENCES Ingredients (ingredient_name)
);

CREATE TABLE RecipeIngredients (
		ingredient_name VARCHAR(32),
        recipe_name VARCHAR(32),
        quantity float,
        PRIMARY KEY (ingredient_name, recipe_name),
        FOREIGN KEY (recipe_name) REFERENCES Recipes (recipe_name),
        FOREIGN KEY (ingredient_name) REFERENCES Ingredients (ingredient_name)
);

CREATE TABLE Pantry (
        ingredient_name VARCHAR(32),
        username VARCHAR(32),
		quantity float,
        PRIMARY KEY (ingredient_name, username),
        FOREIGN KEY (username) REFERENCES Person (username),
        FOREIGN KEY (ingredient_name) REFERENCES Ingredients (ingredient_name)
);
