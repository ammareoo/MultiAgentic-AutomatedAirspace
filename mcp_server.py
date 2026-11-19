
from fastapi import FastAPI, HTTPException
import glob, json, os
from fastapi.responses import JSONResponse

SNAPSHOT_DIR = "snapshots"
app = FastAPI(title="MCP Flight Tools")

def list_snapshots(region):
    return sorted(glob.glob(os.path.join(SNAPSHOT_DIR, f"{region}_*.json")), reverse=True)

def load_latest_snapshot(region):
    files = list_snapshots(region)
    if not files:
        return None
    with open(files[0]) as f:
        return json.load(f)

@app.get("/tools/flights.list")
def flights_list(region: str):
    snap = load_latest_snapshot(region)
    if not snap:
        return JSONResponse(status_code=404, content={"error": "No snapshot"})
    return snap

@app.get("/tools/flights.get")
def flights_get(identifier: str):
    files = glob.glob(os.path.join(SNAPSHOT_DIR, "*.json"))
    for fpath in files:
        with open(fpath) as f:
            data = json.load(f)
        for flight in data.get("flights", []):
            if flight.get("callsign") == identifier or flight.get("icao24") == identifier:
                return flight
    raise HTTPException(status_code=404, detail="Flight not found")
