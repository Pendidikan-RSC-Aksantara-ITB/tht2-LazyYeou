<script>
import { onMount } from 'svelte';
import { browser } from '$app/environment';
import 'leaflet/dist/leaflet.css';
import './page-style.css';

let map;
let L;
let waypoints = [];
let aksantaraIcon;
    
const API_URL = "http://localhost:8081/api";

onMount(async () => {
    if (browser) {
    L = await import('leaflet');
    map = L.map('map').setView([-6.8915, 107.6107], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap'
    }).addTo(map);

    aksantaraIcon = L.icon({
        iconUrl: '/aksantara.svg',
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
    });

    // click event
    map.on('click', (e) => {
        addWaypoint(e.latlng.lat, e.latlng.lng);
        console.log(e);
    });
    fetchWaypoints();
}
});

async function fetchWaypoints() {
    try {
        const res = await fetch(`${API_URL}/waypoints`);
        if (res.ok) {
            const data = await res.json();
            waypoints = data.map(wp => ({...wp, markerRef: null})); 
        }
    } catch (e) { 
        console.error("be aman?", e);
        alert("gagal konek be"); 
    }
}

function addWaypoint(lat, lon) {
    waypoints = [...waypoints, {
        id: crypto.randomUUID(),
        name: `weipoin ${waypoints.length + 1}`,
        latitude: lat,
        longitude: lon,
        altitude: 100,
        markerRef: null
    }];
}

function deleteWaypoint(id) {
    const wp = waypoints.find(w => w.id === id);
    if (wp?.markerRef) map.removeLayer(wp.markerRef);
    waypoints = waypoints.filter(w => w.id !== id);
}

async function save() {
    const pl = waypoints.map(({ markerRef, ...rest }) => rest);
    
    console.log("senda data:", JSON.stringify(pl, null, 2));

    for (let i = 0; i < pl.length; i++) {
        if (!pl[i].name || pl[i].name.trim() === "") {
            alert(`err: nama waypoint ${i+1} kosong`);
            return;
        }
    }

    try {
        const res = await fetch(`${API_URL}/waypoints`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pl)
        });
        
        if (res.ok) {
            alert("tersimpan di db");
        } else {
            const err = await res.json();
            alert("gagal menyimpan: " + JSON.stringify(err));
        }
    } catch (e) { 
        alert("gagal"); 
    }
}

$: if (map && L) {
    waypoints.forEach(wp => {
    if (!wp.markerRef) {
        const m = L.marker([wp.latitude, wp.longitude], { icon: aksantaraIcon })
        .addTo(map)
        .bindPopup(`<b>${wp.name}</b><br>Lat: ${wp.latitude.toFixed(2)}<br>Lon: ${wp.longitude.toFixed(2)}`);
        
        wp.markerRef = m;
    }
    });
}
</script>

<div class="container">
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>GCS Aseli Ngawi</h1>
            <button on:click={save} class="btn-save">simpan ke db</button>
        </div>
        
        <div class="wp-list-container">
            {#if waypoints.length === 0}
            <p style="color: gray; text-align: center;">buat waypoint dulu wok</p>
            {/if}
            
            {#each waypoints as wp}
            <div class="waypoint-button">
                <input type="text" bind:value={wp.name} placeholder="nama waypoint" />
                
                <div class="coord">
                    Lat: {wp.latitude.toFixed(4)}
                    <br/>
                    Lon: {wp.longitude.toFixed(4)}
                </div>
                
                <div class="coord">
                    Alt: <input type="number" bind:value={wp.altitude} />
                </div>

            <button on:click={() => deleteWaypoint(wp.id)} class="btn-delete">
                Hapus weipoin
            </button>
            </div>
            {/each}
        </div>
    </div>

    <div class="map-section">
        <div id="map"></div>
    </div>
</div>