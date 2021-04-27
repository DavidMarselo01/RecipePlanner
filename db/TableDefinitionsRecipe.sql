CREATE TABLE Recipes (
        rID INT AUTO_INCREMENT,
        username VARCHAR(32),
        name VARCHAR(32),
        instructions VARCHAR(1000),
        cook_time INT,
		PRIMARY KEY (rID),
        FOREIGN KEY (username) REFERENCES Person (username)
);

CREATE TABLE Ingredients (
        iID INT AUTO_INCREMENT,
        name VARCHAR(32),
        alias VARCHAR(32),
		PRIMARY KEY (iID)
);

CREATE TABLE Pantry (
		pID INT AUTO_INCREMENT,
        iID INT,
        username VARCHAR(32),
		PRIMARY KEY (pID),
        FOREIGN KEY (username) REFERENCES Person (username),
        FOREIGN KEY (iID) REFERENCES Ingredients (iID)
);

CREATE TABLE measurement_units (
		measurement_id INT AUTO_INCREMENT,
        description VARCHAR(32),
		PRIMARY KEY (measurement_id)
);

CREATE TABLE measurement_qty (
		measurement_qty_id INT AUTO_INCREMENT,
        description VARCHAR(32),
		PRIMARY KEY (measurement_qty_id)
);

CREATE TABLE RecipeIngredients (
		iID INT,
        rID INT,
        measurement_id INT,
        measurement_qty_id INT,
		PRIMARY KEY (rID, iID),
        FOREIGN KEY (rID) REFERENCES Recipes (rID),
        FOREIGN KEY (iID) REFERENCES Ingredients (iID),
        FOREIGN KEY (measurement_id) REFERENCES measurement_units (measurement_id),
        FOREIGN KEY (measurement_qty_id) REFERENCES measurement_qty (measurement_qty_id)
);

CREATE TABLE tag (
		tag_name VARCHAR(32),
		rID INT,
        username VARCHAR(32),
		PRIMARY KEY (tag_name),
        FOREIGN KEY (rID) REFERENCES Recipes (rID),
        FOREIGN KEY (username) REFERENCES Person (username)
);
