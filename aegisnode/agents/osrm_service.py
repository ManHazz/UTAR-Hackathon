"""
AegisNode - OSRM Route Verification Service
Interacts with the OpenStreetMap OSRM routing engine to verify physical travel feasibility.
Includes intelligent local route caching and Haversine physics fallback for fail-safe hackathon reliability.
"""

import math
import logging
import requests
from typing import Tuple, Dict, Any, List

logger = logging.getLogger(__name__)

# Pre-baked travel metrics for GDEX demonstration routes (Shah Alam <-> PJ / Klang Valley)
# Ensures 100% demo reliability even if the presentation room has spotty Wi-Fi
PREBAKED_ROUTES = {
    # Shah Alam Central Hub to PJ SS2 (approx 14.8 km driving, ~24 mins)
    "3.0738,101.5385->3.1186,101.6214": {"distance_km": 14.8, "duration_seconds": 1440},
    # Shah Alam Section 23 Industrial to Menara PJX (approx 15.2 km driving, ~26 mins)
    "3.0450,101.5200->3.1032,101.6445": {"distance_km": 15.2, "duration_seconds": 1560},
    # Hub to Federal Highway Batu Tiga (~5.5 km, ~8 mins)
    "3.0738,101.5385->3.0912,101.5794": {"distance_km": 5.5, "duration_seconds": 480},
    # Batu Tiga to Kelana Jaya (~6.8 km, ~12 mins)
    "3.0912,101.5794->3.1070,101.6030": {"distance_km": 6.8, "duration_seconds": 720},
    # Kelana Jaya to PJ SS2 (~3.2 km, ~7 mins)
    "3.1070,101.6030->3.1186,101.6214": {"distance_km": 3.2, "duration_seconds": 420},
    # Bangsar Approach to Bangsar Residence (~1.8 km, ~4 mins)
    "3.1250,101.6620->3.1319,101.6705": {"distance_km": 1.8, "duration_seconds": 240},
}

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# In-memory session cache for retrieved route coordinates
_ROUTE_CACHE: Dict[str, Dict[str, Any]] = {}

def check_route_feasibility(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    timeout_sec: float = 3.0
) -> Dict[str, Any]:
    """
    Queries OpenStreetMap OSRM routing engine to determine realistic driving travel time,
    distance, and road coordinate geometry. Falls back gracefully to pre-baked demo cache or physics.
    """
    route_key = f"{lat1:.4f},{lon1:.4f}->{lat2:.4f},{lon2:.4f}"
    
    # 0. Check in-memory session cache
    if route_key in _ROUTE_CACHE:
        return _ROUTE_CACHE[route_key]

    # 1. Try Live Public OSRM API (100% Free, no API key needed)
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
        resp = requests.get(url, timeout=timeout_sec)
        if resp.status_code == 200:
            data = resp.json()
            if "routes" in data and len(data["routes"]) > 0:
                duration_sec = float(data["routes"][0]["duration"])
                dist_km = float(data["routes"][0]["distance"]) / 1000.0
                raw_coords = data["routes"][0].get("geometry", {}).get("coordinates", [])
                geometry = [[p[1], p[0]] for p in raw_coords] if raw_coords else [[lat1, lon1], [lat2, lon2]]
                res = {
                    "distance_km": round(dist_km, 2),
                    "duration_seconds": int(duration_sec),
                    "duration_minutes": round(duration_sec / 60.0, 1),
                    "geometry": geometry,
                    "source": "LIVE_OSRM"
                }
                _ROUTE_CACHE[route_key] = res
                return res
    except Exception as e:
        logger.warning(f"OSRM live request failed: {e}. Falling back to cache/physics.")

    # 2. Check Pre-baked Cache for Demo Reliability
    if route_key in PREBAKED_ROUTES:
        cached = PREBAKED_ROUTES[route_key]
        return {
            "distance_km": cached["distance_km"],
            "duration_seconds": cached["duration_seconds"],
            "duration_minutes": round(cached["duration_seconds"] / 60.0, 1),
            "geometry": [[lat1, lon1], [lat2, lon2]],
            "source": "PREBAKED_CACHE"
        }

    # 3. Physics-based fallback (Assumes 40 km/h average Klang Valley city speed with 1.35x road winding factor)
    haversine_km = haversine_distance_km(lat1, lon1, lat2, lon2)
    estimated_driving_km = haversine_km * 1.35
    estimated_duration_sec = (estimated_driving_km / 40.0) * 3600.0

    return {
        "distance_km": round(estimated_driving_km, 2),
        "duration_seconds": int(estimated_duration_sec),
        "duration_minutes": round(estimated_duration_sec / 60.0, 1),
        "geometry": [[lat1, lon1], [lat2, lon2]],
        "source": "PHYSICS_ESTIMATION"
    }

def get_leg_route_geometry(lat1: float, lon1: float, lat2: float, lon2: float) -> List[List[float]]:
    """Helper to retrieve real road polyline geometry between two checkpoints."""
    res = check_route_feasibility(lat1, lon1, lat2, lon2)
    return res.get("geometry", [[lat1, lon1], [lat2, lon2]])

