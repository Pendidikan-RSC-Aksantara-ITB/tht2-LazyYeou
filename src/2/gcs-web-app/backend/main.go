package main

import (
	_ "github.com/mattn/go-sqlite3"
)

type Waypoint struct {
	ID        string  `json:"id" binding:"required"`
	Name      string  `json:"string" binding:"required"`
	Longitude float64 `json:"longitude" binding:"required,min=-180,max=190"`
	Latitude  float64 `json:"latitude" binding:"required,min=-90,max=190"`
	Altitude  float64 `json:"altitude" binding:"required,min=0"`
}
