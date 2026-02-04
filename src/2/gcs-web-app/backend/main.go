package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
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

func initDB() {
	dbPath := os.Getenv("DB_PATH")
	if dbPath == "" {
		dbPath = "/data/waypoints.db"
	}

	db, err := sql.Open("sqlite3", dbPath)
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

	_, err = db.Exec(createTableSQL)
	if err != nil {
		log.Fatal(err)
	}
}

func getWaypoints(c *gin.Context) {
	rows, err := db.Query("SELECT id, name, longitude, latitude, altitude FROM waypoints")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"err": err.Error()})
		return
	}
	defer rows.Close()

	waypoints := []Waypoint{}
	for rows.Next() {
		var w Waypoint
		err := rows.Scan(&w.ID, &w.Name, &w.Longitude, &w.Latitude, &w.Altitude)
		if err != nil {
			return
		}
		waypoints = append(waypoints, w)
	}
	c.JSON(http.StatusOK, waypoints)
}

func saveWaypoints(c *gin.Context) {

}

func main() {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	port := "8081"
	r.Run(":" + port)
}
