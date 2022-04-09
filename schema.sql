DROP TABLE IF EXISTS mountains;

CREATE TABLE "Mountains" (
	"mountainid"	INTEGER NOT NULL,
	"osmfilename"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"location"	TEXT NOT NULL,
	"direction"	TEXT NOT NULL,
	"trailcount"	INTEGER NOT NULL,
	"liftcount"	INTEGER NOT NULL,
	"vertical"	REAL NOT NULL,
	"difficulty"	REAL NOT NULL,
	"beginnerfriendliness"	REAL NOT NULL,
	PRIMARY KEY("mountainid" AUTOINCREMENT)
)


DROP TABLE IF EXISTS Trails;

CREATE TABLE "Trails" (
	"trailid"	INTEGER NOT NULL,
	"mountainid"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"isarea"	INTEGER NOT NULL,
	"difficulty"	REAL NOT NULL,
	"difficultymodifier"	REAL NOT NULL,
	"steepestpitch"	REAL NOT NULL,
	"verticaldrop"	INTEGER NOT NULL,
	"length"	REAL NOT NULL,
	PRIMARY KEY("trailid" AUTOINCREMENT),
	FOREIGN KEY("mountainid") REFERENCES "Mountains"("mountainid") ON DELETE CASCADE
)


DROP TABLE IF EXISTS Lifts;

CREATE TABLE "Lifts" (
	"liftid"	INTEGER NOT NULL,
	"mountainid"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("liftid" AUTOINCREMENT),
	FOREIGN KEY("mountainid") REFERENCES "Mountains"("mountainid") ON DELETE CASCADE
)


DROP TABLE IF EXISTS TrailPoints;

CREATE TABLE "TrailPoints" (
	"index"	INTEGER NOT NULL,
	"trailid"	INTEGER NOT NULL,
	"fordisplay"	INTEGER NOT NULL,
	"latitude"	REAL NOT NULL,
	"longitude"	REAL NOT NULL,
	"elevation"	REAL NOT NULL,
	"slope"	REAL NOT NULL,
	PRIMARY KEY("index","trailid"),
	FOREIGN KEY("trailid") REFERENCES "Trails"("trailid") ON DELETE CASCADE
)


DROP TABLE IF EXISTS LiftPoints;

CREATE TABLE "LiftPoints" (
	"index"	INTEGER NOT NULL,
	"liftid"	INTEGER NOT NULL,
	"latitude"	REAL NOT NULL,
	"longitude"	REAL NOT NULL,
	"elevation"	REAL NOT NULL,
	PRIMARY KEY("index","liftid"),
	FOREIGN KEY("liftid") REFERENCES "Lifts"("liftid") ON DELETE CASCADE
)


