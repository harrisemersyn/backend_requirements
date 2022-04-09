DROP TABLE IF EXISTS Mountains;

CREATE TABLE "Mountains" (
	"mountainid"	INTEGER NOT NULL,
	"osm_file_name"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"state"	TEXT NOT NULL,
	"direction"	TEXT NOT NULL,
	"trail_count"	INTEGER NOT NULL,
	"lift_count"	INTEGER NOT NULL,
	"vertical"	REAL NOT NULL,
	"difficulty"	REAL NOT NULL,
	"beginner_friendliness"	REAL NOT NULL,
	PRIMARY KEY("mountainid" AUTOINCREMENT)
);


DROP TABLE IF EXISTS Trails;

CREATE TABLE "Trails" (
	"trailid"	INTEGER NOT NULL,
	"mountainid"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"is_area"	INTEGER NOT NULL,
	"difficulty"	REAL NOT NULL,
	"difficulty_modifier"	REAL NOT NULL,
	"steepest_pitch"	REAL NOT NULL,
	"vertical_drop"	INTEGER NOT NULL,
	"length"	REAL NOT NULL,
	PRIMARY KEY("trailid" AUTOINCREMENT),
	FOREIGN KEY("mountainid") REFERENCES "Mountains"("mountainid") ON DELETE CASCADE
);


DROP TABLE IF EXISTS Lifts;

CREATE TABLE "Lifts" (
	"liftid"	INTEGER NOT NULL,
	"mountainid"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("liftid" AUTOINCREMENT),
	FOREIGN KEY("mountainid") REFERENCES "Mountains"("mountainid") ON DELETE CASCADE
);


DROP TABLE IF EXISTS TrailPoints;

CREATE TABLE "TrailPoints" (
	"index"	INTEGER NOT NULL,
	"trailid"	INTEGER NOT NULL,
	"for_display"	INTEGER NOT NULL,
	"latitude"	REAL NOT NULL,
	"longitude"	REAL NOT NULL,
	"elevation"	REAL NOT NULL,
	"slope"	REAL NOT NULL,
	PRIMARY KEY("index","trailid"),
	FOREIGN KEY("trailid") REFERENCES "Trails"("trailid") ON DELETE CASCADE
);


DROP TABLE IF EXISTS LiftPoints;

CREATE TABLE "LiftPoints" (
	"index"	INTEGER NOT NULL,
	"liftid"	INTEGER NOT NULL,
	"latitude"	REAL NOT NULL,
	"longitude"	REAL NOT NULL,
	"elevation"	REAL NOT NULL,
	PRIMARY KEY("index","liftid"),
	FOREIGN KEY("liftid") REFERENCES "Lifts"("liftid") ON DELETE CASCADE
);


