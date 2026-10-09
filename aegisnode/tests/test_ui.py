"""
Unit tests for AegisNode UI components and visualizers
"""

import json
from pathlib import Path
from aegisnode.ui.styles import get_custom_css
from aegisnode.ui.charts import (
    build_gauge_chart,
    build_route_feasibility_chart,
    build_api_threat_chart,
    build_penalty_breakdown_chart,
)

DATA_DIR = Path(__file__).parent.parent / "data"

def test_custom_css_generation():
    css = get_custom_css()
    assert isinstance(css, str)
    assert "<style>" in css
    assert "command-header" in css
    assert "cyber-kpi" in css
    assert "agent-card" in css

def test_gauge_chart_thresholds():
    # Low score (freeze)
    fig_low = build_gauge_chart(18)
    assert fig_low is not None
    assert fig_low.data[0].value == 18

    # Medium score (OTP)
    fig_med = build_gauge_chart(55)
    assert fig_med is not None
    assert fig_med.data[0].value == 55

    # High score (Clear)
    fig_high = build_gauge_chart(95)
    assert fig_high is not None
    assert fig_high.data[0].value == 95

def test_route_feasibility_chart():
    # Empty evaluations
    fig_empty = build_route_feasibility_chart([])
    assert fig_empty is not None

    # Realistic evaluations
    sample_evals = [
        {
            "segment": "Event 1 -> Event 2",
            "actual_elapsed_min": 15.0,
            "osrm_expected_min": 18.0,
            "is_impossible": False
        },
        {
            "segment": "Event 2 -> Event 3",
            "actual_elapsed_min": 2.0,
            "osrm_expected_min": 26.0,
            "is_impossible": True
        }
    ]
    fig = build_route_feasibility_chart(sample_evals)
    assert fig is not None
    assert len(fig.data) == 2  # Expected and Actual traces

def test_api_threat_chart():
    with open(DATA_DIR / "fraud_api_scraping.json", "r", encoding="utf-8") as f:
        scenario_data = json.load(f)

    fig = build_api_threat_chart(scenario_data)
    assert fig is not None
    assert len(fig.data) >= 2  # Rate limit line and surge scatter

def test_penalty_breakdown_chart():
    penalties = {
        "kinematic_road_violation": 60,
        "telematics_spoof": 35,
        "pod_forgery": 0,
        "value_multiplier": 1.35
    }
    fig = build_penalty_breakdown_chart(penalties, 5)
    assert fig is not None
    assert len(fig.data) >= 1

def test_live_bridge_sync():
    from aegisnode.data.live_bridge import (
        get_live_state,
        update_courier_action,
        update_warden_state,
        reset_live_state,
    )
    # Reset and test default state
    reset_live_state()
    state = get_live_state()
    assert state is not None
    assert "active_scenario" in state

    # Trigger GPS Spoof
    s_spoof = update_courier_action("TRIGGER_GPS_SPOOF", "fraud_gps_spoof.json")
    assert s_spoof["warden_action"] == "PACKAGE_FREEZE"
    assert s_spoof["trust_score"] == 18

    # Trigger OTP Challenge
    s_otp = update_courier_action("SUBMIT_OTP", "fraud_pod_spoof.json", otp_code="849201")
    assert s_otp["otp_verified"] is True
    assert s_otp["warden_action"] == "AUTO_CLEAR"

    # Clean up
    reset_live_state()

def test_phone_hardware_telematics_update():
    from aegisnode.data.live_bridge import update_courier_telematics, get_live_state, reset_live_state
    reset_live_state()
    # Simulate hardware GPS coordinates acquired at UTP Tronoh campus
    st_update = update_courier_telematics(4.385210, 100.978120, label="UTP Tronoh Campus", accuracy_m=8.5)
    assert st_update["courier_lat"] == 4.38521
    assert st_update["courier_lon"] == 100.97812
    assert "UTP" in st_update["courier_location_label"]
    assert st_update["courier_accuracy_m"] == 8.5
    reset_live_state()

def test_gps_spoof_haversine_calculation():
    from aegisnode.data.live_bridge import trigger_gps_spoof, reset_live_state
    reset_live_state()
    # Jump from UTP Campus (4.3852, 100.9781) to Menara PJX (3.1032, 101.6445)
    res = trigger_gps_spoof(
        start_lat=4.3852,
        start_lon=100.9781,
        target_lat=3.1032,
        target_lon=101.6445,
        start_label="UTP Campus",
        target_label="Menara PJX"
    )
    assert res["warden_action"] == "PACKAGE_FREEZE"
    assert res["trust_score"] == 18
    # Distance is ~185 km, simulated in 2 minutes -> velocity > 5000 km/h
    assert res["highest_velocity_kmh"] > 1000.0
    assert res["spoof_distance_km"] > 150.0
    reset_live_state()

def test_live_camera_photo_forensic_analysis():
    import numpy as np
    import cv2
    from aegisnode.data.live_bridge import process_uploaded_pod_photo, reset_live_state
    reset_live_state()

    # 1. Dark floor mat / obstructed sensor test (Low luminance, zero texture)
    dark_img = np.zeros((200, 200, 3), dtype=np.uint8)
    _, dark_encoded = cv2.imencode(".jpg", dark_img)
    res_dark = process_uploaded_pod_photo(dark_encoded.tobytes())
    assert res_dark["live_photo_status"] == "FORGED"
    assert res_dark["warden_action"] == "STEP_UP_CHALLENGE"
    assert res_dark["trust_score"] < 50
    assert res_dark["has_live_photo"] is True

    # 2. High-contrast, well-lit parcel test (Ambient light > 100, clear edges)
    bright_img = np.full((200, 200, 3), 180, dtype=np.uint8)
    cv2.rectangle(bright_img, (20, 20), (180, 180), (30, 30, 30), 3)
    cv2.putText(bright_img, "GDEX PARCEL #042", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 10, 10), 2)
    _, bright_encoded = cv2.imencode(".jpg", bright_img)
    res_bright = process_uploaded_pod_photo(bright_encoded.tobytes())
    assert res_bright["live_photo_status"] == "VALID"
    assert res_bright["warden_action"] == "AUTO_CLEAR"
    assert res_bright["trust_score"] > 90

    reset_live_state()



