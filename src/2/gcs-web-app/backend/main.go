package main

import (
	"os"
	"database/sql"

	_ "github.com/mattn/go-sqlite3"
)

type Waypoint struct {
	ID        string  `json:"id" binding:"required"`
	Name      string  `json:"string" binding:"required"`
	Longitude float64 `json:"longitude" binding:"required,min=-180,max=190"`
	Latitude  float64 `json:"latitude" binding:"required,min=-90,max=190"`
	Altitude  float64 `json:"altitude" binding:"required,min=0"`
}

var db *sql.DB

dbPath := os.GetEnv("DB_PATH")
if dbPath == "" {
	dbPath = "/data/waypoints.db"
}

db, err = sql.Open("sqlite3", dbPath)
if err != nil {
	log.Fatal(err)
}

createTableSQL := `CREATE TABLE IF NOT EXISTS waypoints (
	id TEXT PRIMARY KEY,
	name TEXT NOT NULL,
	longitude REAL NOT NULL,
	latitude REAL NOT NULL,
	altitude REAL NOT NULL
);`

x, err = db.Exec(createTableSQL)
if err != nil {
	log.Fatal(err)
}

