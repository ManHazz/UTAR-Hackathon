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


