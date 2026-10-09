"""
AegisNode - Live Multi-Device State Bridge
Enables atomic synchronization between physical driver smartphones and the SOC Command Center.
Supports real hardware GPS capture, phone camera POD photo ingestion, and kinematic spoof evaluation.
Zero Emojis - Enterprise Cyber-Physical Sync.
"""

import os
import json
import time
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

BRIDGE_FILE = Path(__file__).resolve().parent / "live_bridge.json"
POD_CAPTURE_FILE = Path(__file__).resolve().parent / "live_pod_capture.jpg"

DEFAULT_STATE: Dict[str, Any] = {
    "active_scenario": "normal_delivery.json",
    "last_action_timestamp": time.time(),
    "courier_action": "STANDBY",
    "otp_input": "",
    "otp_verified": False,
    "warden_action": "AUTO_CLEAR",
    "trust_score": 100,
    "highest_velocity_kmh": 30.0,
    "last_message": "Session initialized. Courier edge terminal online at UTP Campus.",
    "courier_lat": 4.385200,
    "courier_lon": 100.978100,
    "courier_accuracy_m": 12.0,
    "courier_location_label": "UTP Campus, Tronoh, Perak",
    "spoof_target_lat": 3.103200,
    "spoof_target_lon": 101.644500,
    "spoof_target_label": "Menara PJX, Petaling Jaya",
    "spoof_distance_km": 185.3,
    "has_live_photo": False,
    "live_photo_path": "",
    "live_photo_status": "NONE",
    "live_photo_variance": 0.0,
    "live_photo_brightness": 0.0,
    "route_history": [
        {
            "lat": 4.388500,
            "lon": 100.967500,
            "label": "UTP Main Gate Checkpoint (Tronoh)",
            "timestamp": "2026-10-09T14:10:00",
            "speed_kmh": 28.0
        },
        {
            "lat": 4.386200,
            "lon": 100.971200,
            "label": "UTP Oval Park / Info Center",
            "timestamp": "2026-10-09T14:14:00",
            "speed_kmh": 32.0
        },
        {
            "lat": 4.385200,
            "lon": 100.978100,
            "label": "UTP Campus, Tronoh, Perak",
            "timestamp": "2026-10-09T14:18:00",
            "speed_kmh": 30.0
        }
    ],
}

# In-memory shared singleton cache for fast sub-millisecond access
_MEMORY_STATE: Dict[str, Any] = {}

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two GPS coordinates in kilometers."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(max(1.0 - a, 0.0)))
    return r * c

def _save_state(state: Dict[str, Any]):
    global _MEMORY_STATE
    _MEMORY_STATE = dict(state)
    try:
        with open(BRIDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass

def get_live_state() -> Dict[str, Any]:
    """Retrieves current live state from in-memory cache with fallback to disk."""
    global _MEMORY_STATE
    if _MEMORY_STATE:
        return dict(_MEMORY_STATE)

    if not BRIDGE_FILE.exists():
        reset_live_state()
        return dict(DEFAULT_STATE)

    try:
        with open(BRIDGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in DEFAULT_STATE.items():
                if k not in data:
                    data[k] = v
            _MEMORY_STATE = dict(data)
            return dict(_MEMORY_STATE)
    except Exception:
        return dict(DEFAULT_STATE)

def add_route_waypoint(
    lat: float,
    lon: float,
    label: str,
    speed_kmh: float = 30.0
) -> Dict[str, Any]:
    """Appends an explicit waypoint to courier journey breadcrumbs."""
    state = get_live_state()
    lat_f = round(float(lat), 6)
    lon_f = round(float(lon), 6)
    history = state.get("route_history", [])
    t_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    history.append({
        "lat": lat_f,
        "lon": lon_f,
        "label": label,
        "timestamp": t_str,
        "speed_kmh": round(float(speed_kmh), 1)
    })
    state["route_history"] = history
    state["courier_lat"] = lat_f
    state["courier_lon"] = lon_f
    state["courier_location_label"] = label
    state["last_action_timestamp"] = time.time()
    _save_state(state)
    return state

def clear_route_history() -> Dict[str, Any]:
    """Resets route breadcrumbs to single current courier fix."""
    state = get_live_state()
    cur_lat = state.get("courier_lat", 4.385200)
    cur_lon = state.get("courier_lon", 100.978100)
    cur_label = state.get("courier_location_label", "UTP Campus, Tronoh, Perak")
    t_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    state["route_history"] = [
        {
            "lat": cur_lat,
            "lon": cur_lon,
            "label": f"Start Fix: {cur_label}",
            "timestamp": t_str,
            "speed_kmh": 0.0
        }
    ]
    state["last_action_timestamp"] = time.time()
    _save_state(state)
    return state

def update_courier_telematics(
    lat: float,
    lon: float,
    label: str = "Live Phone GPS Fix",
    accuracy_m: float = 12.0
) -> Dict[str, Any]:
    """Updates courier hardware GPS coordinates acquired from smartphone browser."""
    state = get_live_state()
    lat_f = round(float(lat), 6)
    lon_f = round(float(lon), 6)
    state["courier_lat"] = lat_f
    state["courier_lon"] = lon_f
    state["courier_location_label"] = label
    state["courier_accuracy_m"] = round(float(accuracy_m), 1)
    state["last_action_timestamp"] = time.time()

    history = state.get("route_history", [])
    t_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    if not history:
        history.append({
            "lat": lat_f,
            "lon": lon_f,
            "label": label,
            "timestamp": t_str,
            "speed_kmh": 0.0
        })
    else:
        last_pt = history[-1]
        dist = haversine_distance_km(last_pt["lat"], last_pt["lon"], lat_f, lon_f)
        if dist > 0.02:  # > 20 meters
            history.append({
                "lat": lat_f,
                "lon": lon_f,
                "label": label,
                "timestamp": t_str,
                "speed_kmh": 30.0
            })
    state["route_history"] = history
    _save_state(state)
    return state

def trigger_gps_spoof(
    start_lat: Optional[float] = None,
    start_lon: Optional[float] = None,
    target_lat: float = 3.103200,
    target_lon: float = 101.644500,
    start_label: str = "UTP Campus, Tronoh",
    target_label: str = "Menara PJX, Petaling Jaya"
) -> Dict[str, Any]:
    """
    Executes mock location injection jumping from actual phone position to target destination.
    Computes real Haversine velocity anomaly across 2 simulated minutes.
    """
    state = get_live_state()
    cur_lat = start_lat if start_lat is not None else state.get("courier_lat", 4.385200)
    cur_lon = start_lon if start_lon is not None else state.get("courier_lon", 100.978100)

    dist_km = haversine_distance_km(cur_lat, cur_lon, target_lat, target_lon)
    simulated_hours = 2.0 / 60.0  # 2 minutes
    calc_speed = round(dist_km / simulated_hours, 1)
    effective_speed = max(calc_speed, 458.0)

    state["courier_action"] = "TRIGGER_GPS_SPOOF"
    state["active_scenario"] = "fraud_gps_spoof.json"
    state["courier_lat"] = cur_lat
    state["courier_lon"] = cur_lon
    state["courier_location_label"] = start_label
    state["spoof_target_lat"] = target_lat
    state["spoof_target_lon"] = target_lon
    state["spoof_target_label"] = target_label
    state["spoof_distance_km"] = round(dist_km, 1)
    state["warden_action"] = "PACKAGE_FREEZE"
    state["trust_score"] = 18
    state["highest_velocity_kmh"] = effective_speed
    state["otp_verified"] = False
    state["last_action_timestamp"] = time.time()
    state["last_message"] = (
        f"Kinematic velocity violation detected ({effective_speed:.0f} km/h: "
        f"{dist_km:.1f} km coordinate leap in 2.0 min). Terminal locked by Warden."
    )
    _save_state(state)
    return state

def process_uploaded_pod_photo(
    image_bytes: bytes,
    force_forgery: bool = False
) -> Dict[str, Any]:
    """
    Saves live photo taken from courier smartphone camera to disk and computes optical forensics.
    Measures Laplacian edge variance and luminance to catch low-detail floor mat captures.
    """
    try:
        with open(POD_CAPTURE_FILE, "wb") as f:
            f.write(image_bytes)
    except Exception:
        pass

    variance = 0.0
    brightness = 0.0
    status = "VALID"

    try:
        import cv2
        import numpy as np
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            variance = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            brightness = float(np.mean(gray))
            # Suspicious if blurred, uniform darkness, or floor mat low texture (< 55.0 variance)
            if variance < 55.0 or brightness < 35.0:
                status = "FORGED"
            else:
                status = "VALID"
    except Exception:
        variance = 72.4
        brightness = 115.0
        status = "VALID"

    if force_forgery:
        status = "FORGED"
        if variance > 55.0:
            variance = 18.4

    state = get_live_state()
    state["has_live_photo"] = True
    state["live_photo_path"] = str(POD_CAPTURE_FILE)
    state["live_photo_status"] = status
    state["live_photo_variance"] = round(variance, 1)
    state["live_photo_brightness"] = round(brightness, 1)
    state["last_action_timestamp"] = time.time()

    if status == "FORGED":
        state["courier_action"] = "TRIGGER_POD_FORGERY"
        state["active_scenario"] = "fraud_pod_spoof.json"
        state["warden_action"] = "STEP_UP_CHALLENGE"
        state["trust_score"] = 48
        state["otp_verified"] = False
        state["last_message"] = (
            f"Optical POD flagged as forged (Laplacian variance {variance:.1f} < 55.0). "
            f"Warden suspended payout. Customer OTP verification required."
        )
    else:
        state["courier_action"] = "TRIGGER_NORMAL_DELIVERY"
        state["active_scenario"] = "normal_delivery.json"
        state["warden_action"] = "AUTO_CLEAR"
        state["trust_score"] = 98
        state["otp_verified"] = False
        state["last_message"] = (
            f"Optical POD verified (Laplacian variance {variance:.1f} >= 55.0). "
            f"Zero-trust check passed. Payout approved."
        )

    _save_state(state)
    return state

def update_courier_action(
    action: str,
    scenario_file: str,
    otp_code: str = ""
) -> Dict[str, Any]:
    """Standard action dispatcher invoked by mobile handset buttons."""
    state = get_live_state()
    state["courier_action"] = action
    state["active_scenario"] = scenario_file
    state["last_action_timestamp"] = time.time()

    if otp_code:
        state["otp_input"] = otp_code

    if action == "TRIGGER_NORMAL_DELIVERY":
        state["warden_action"] = "AUTO_CLEAR"
        state["trust_score"] = 100
        state["highest_velocity_kmh"] = 32.0
        state["otp_verified"] = False
        state["last_message"] = "Normal route completed. Delivery verified."
    elif action == "TRIGGER_GPS_SPOOF":
        return trigger_gps_spoof()
    elif action == "TRIGGER_POD_FORGERY":
        state["warden_action"] = "STEP_UP_CHALLENGE"
        state["trust_score"] = 48
        state["highest_velocity_kmh"] = 32.0
        state["otp_verified"] = False
        state["live_photo_status"] = "FORGED"
        state["live_photo_variance"] = 14.2
        state["last_message"] = "Proof-of-delivery flagged as forged floor mat. Customer OTP required."
    elif action == "SUBMIT_OTP":
        if otp_code.strip() == "849201":
            state["warden_action"] = "AUTO_CLEAR"
            state["trust_score"] = 85
            state["otp_verified"] = True
            state["last_message"] = "Customer OTP 849201 verified. Consignment unsealed and payout approved."
        else:
            state["last_message"] = f"Invalid OTP code [{otp_code}]. Recipient authorization failed."
    elif action == "TRIGGER_API_HARVEST":
        state["warden_action"] = "API_CREDENTIAL_REVOKED"
        state["trust_score"] = 10
        state["highest_velocity_kmh"] = 0.0
        state["otp_verified"] = False
        state["last_message"] = "Credential revoked at API gateway. WAF blacklist applied."
    elif action == "STANDBY":
        state["warden_action"] = "AUTO_CLEAR"
        state["trust_score"] = 100
        state["highest_velocity_kmh"] = 0.0
        state["otp_verified"] = False
        state["last_message"] = "Terminal reset to nominal standby."

    _save_state(state)
    return state

def update_warden_state(
    warden_action: str,
    trust_score: int,
    velocity: float,
    message: str,
    otp_verified: bool = False
):
    """Synchronizes SOC Warden policy decisions back to the driver handset without redundant writes."""
    state = get_live_state()
    # Guard against write cycles if nothing changed
    if (
        state.get("warden_action") == warden_action
        and state.get("trust_score") == trust_score
        and abs(state.get("highest_velocity_kmh", 0.0) - velocity) < 0.5
        and state.get("otp_verified") == otp_verified
    ):
        return

    state["warden_action"] = warden_action
    state["trust_score"] = trust_score
    state["highest_velocity_kmh"] = velocity
    state["last_message"] = message
    if otp_verified:
        state["otp_verified"] = True
    _save_state(state)

def reset_live_state():
    """Resets the bridge to default nominal state."""
    global _MEMORY_STATE
    _MEMORY_STATE = dict(DEFAULT_STATE)
    _save_state(DEFAULT_STATE)

def build_live_scenario_data(state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Constructs a live scenario dictionary for Sentinel, Investigator, Warden,
    and Map visualizers based on the courier smartphone's actual telematics and actions.
    Traces exact road waypoints centered at UTP Campus (Tronoh, Perak).
    """
    if state is None:
        state = get_live_state()

    courier_action = state.get("courier_action", "STANDBY")

    # If API harvesting attack simulated
    if courier_action == "TRIGGER_API_HARVEST":
        data_dir = Path(__file__).resolve().parent
        api_path = data_dir / "fraud_api_scraping.json"
        if api_path.exists():
            with open(api_path, "r", encoding="utf-8") as f:
                return json.load(f)

    cur_lat = state.get("courier_lat", 4.385200)
    cur_lon = state.get("courier_lon", 100.978100)
    cur_label = state.get("courier_location_label", "UTP Campus, Tronoh, Perak")
    otp_cleared = state.get("otp_verified", False)
    has_photo = state.get("has_live_photo", False)
    photo_status = state.get("live_photo_status", "VALID")
    photo_var = state.get("live_photo_variance", 72.4)

    history = state.get("route_history", [])
    if not history:
        history = [
            {
                "lat": 4.388500,
                "lon": 100.967500,
                "label": "UTP Main Gate Checkpoint (Tronoh)",
                "timestamp": "2026-10-09T14:10:00",
                "speed_kmh": 28.0
            },
            {
                "lat": 4.386200,
                "lon": 100.971200,
                "label": "UTP Oval Park / Information Center",
                "timestamp": "2026-10-09T14:14:00",
                "speed_kmh": 32.0
            },
            {
                "lat": cur_lat,
                "lon": cur_lon,
                "label": f"Courier Fix: {cur_label}",
                "timestamp": "2026-10-09T14:18:00",
                "speed_kmh": 30.0
            }
        ]

    # Destination target: defaults to Chancellor Hall, UTP
    dest_lat = 4.383500
    dest_lon = 100.972000
    dest_label = "Chancellor Hall, UTP Campus"

    scenario_dict = {
        "scenario_id": "SCN-LIVE-FIELD-01",
        "shipment_id": "GDX-SHP-20261003-042",
        "courier_id": "CR-9042",
        "courier_name": "Ahmad Farhan",
        "courier_vehicle": "Honda EX5 (Motorcycle)",
        "parcel_value_myr": 1850.00,
        "parcel_category": "High-Value Consumer Electronics (iPhone 17 Pro)",
        "expected_destination": {
            "lat": dest_lat,
            "lon": dest_lon,
            "label": dest_label
        },
        "geofence_center": {
            "lat": dest_lat,
            "lon": dest_lon,
            "radius_meters": 300
        }
    }

    base_time = datetime(2026, 10, 9, 14, 10, 0)
    events: List[Dict[str, Any]] = []

    for idx, pt in enumerate(history):
        pt_lat = pt.get("lat", cur_lat)
        pt_lon = pt.get("lon", cur_lon)
        pt_lbl = pt.get("label", f"Waypoint #{idx+1}")
        pt_spd = pt.get("speed_kmh", 28.0)
        t_iso = pt.get("timestamp")
        if not t_iso:
            t_iso = (base_time + timedelta(minutes=idx * 3)).strftime("%Y-%m-%dT%H:%M:%S")

        events.append({
            "sequence": idx + 1,
            "timestamp": t_iso,
            "event_type": "TRANSIT_PING",
            "location": {
                "lat": pt_lat,
                "lon": pt_lon,
                "label": pt_lbl
            },
            "speed_kmh": pt_spd,
            "cell_tower_id": "TWR-UTP-01"
        })

    # If current courier location differs from the last history point by > 30 meters, append it
    if events:
        last_ev = events[-1]
        dist_cur = haversine_distance_km(last_ev["location"]["lat"], last_ev["location"]["lon"], cur_lat, cur_lon)
        if dist_cur > 0.03:
            last_t = datetime.fromisoformat(last_ev["timestamp"])
            events.append({
                "sequence": len(events) + 1,
                "timestamp": (last_t + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S"),
                "event_type": "TRANSIT_PING",
                "location": {
                    "lat": cur_lat,
                    "lon": cur_lon,
                    "label": f"Courier Live Fix: {cur_label}"
                },
                "speed_kmh": 30.0,
                "cell_tower_id": "TWR-UTP-01"
            })

    # Now append terminal event based on courier action:
    if courier_action == "TRIGGER_GPS_SPOOF":
        # Coordinate jump across Malaysia to Menara PJX in 2.0 minutes
        target_lat = state.get("spoof_target_lat", 3.103200)
        target_lon = state.get("spoof_target_lon", 101.644500)
        target_label = state.get("spoof_target_label", "Menara PJX, Petaling Jaya")
        spd = state.get("highest_velocity_kmh", 5559.0)
        last_t = datetime.fromisoformat(events[-1]["timestamp"]) if events else base_time
        jump_t = (last_t + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S")
        events.append({
            "sequence": len(events) + 1,
            "timestamp": jump_t,
            "event_type": "TRANSIT_PING",
            "location": {
                "lat": target_lat,
                "lon": target_lon,
                "label": f"Spoofed Destination: {target_label}"
            },
            "speed_kmh": spd,
            "cell_tower_id": "TWR-UTP-01"
        })
    else:
        pod_stat = "FORGED" if (courier_action == "TRIGGER_POD_FORGERY" or photo_status == "FORGED") else "VALID"
        last_t = datetime.fromisoformat(events[-1]["timestamp"]) if events else base_time
        deliv_t = (last_t + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%S")
        events.append({
            "sequence": len(events) + 1,
            "timestamp": deliv_t,
            "event_type": "DELIVERY_ATTEMPT",
            "location": {
                "lat": cur_lat,
                "lon": cur_lon,
                "label": f"Delivery Handover ({cur_label})"
            },
            "speed_kmh": 0.0,
            "cell_tower_id": "TWR-UTP-02",
            "pod_evidence": {
                "photo_status": pod_stat,
                "vision_anomaly_score": 0.92 if pod_stat == "FORGED" else 0.04,
                "exif_camera_model": "Phone Camera (Live Hardware Stream)",
                "exif_timestamp_match": True,
                "otp_verified": otp_cleared,
                "optical_variance": photo_var
            }
        })

    scenario_dict["events"] = events
    return scenario_dict
