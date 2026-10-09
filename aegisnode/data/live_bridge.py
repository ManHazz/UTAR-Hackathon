"""
AegisNode - Live Multi-Device State Bridge
Enables atomic sub-second synchronization between physical driver smartphones and the SOC Command Center.
Zero Emojis - Enterprise Cyber-Physical Sync.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

BRIDGE_FILE = Path(__file__).resolve().parent / "live_bridge.json"

DEFAULT_STATE = {
    "active_scenario": "fraud_gps_spoof.json",
    "last_action_timestamp": time.time(),
    "courier_action": "STANDBY",
    "otp_input": "",
    "otp_verified": False,
    "warden_action": "PACKAGE_FREEZE",
    "trust_score": 18,
    "highest_velocity_kmh": 458.0,
    "last_message": "Session initialized. Awaiting courier telematics.",
}

def get_live_state() -> Dict[str, Any]:
    """Retrieves current live synchronization state from disk with fail-safe defaults."""
    if not BRIDGE_FILE.exists():
        reset_live_state()
        return DEFAULT_STATE.copy()
    try:
        with open(BRIDGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all required keys exist
            for k, v in DEFAULT_STATE.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return DEFAULT_STATE.copy()

def update_courier_action(
    action: str,
    scenario_file: str,
    otp_code: str = ""
) -> Dict[str, Any]:
    """Called by mobile handset client when courier taps an action."""
    state = get_live_state()
    state["courier_action"] = action
    state["active_scenario"] = scenario_file
    state["last_action_timestamp"] = time.time()
    if otp_code:
        state["otp_input"] = otp_code
    if action == "TRIGGER_NORMAL_DELIVERY":
        state["warden_action"] = "AUTO_CLEAR"
        state["trust_score"] = 100
        state["highest_velocity_kmh"] = 45.0
        state["otp_verified"] = False
        state["last_message"] = "Normal route completed. Delivery verified."
    elif action == "TRIGGER_GPS_SPOOF":
        state["warden_action"] = "PACKAGE_FREEZE"
        state["trust_score"] = 18
        state["highest_velocity_kmh"] = 458.0
        state["otp_verified"] = False
        state["last_message"] = "Kinematic velocity violation detected (458 km/h). Terminal locked."
    elif action == "TRIGGER_POD_FORGERY":
        state["warden_action"] = "STEP_UP_CHALLENGE"
        state["trust_score"] = 50
        state["highest_velocity_kmh"] = 32.0
        state["otp_verified"] = False
        state["last_message"] = "Proof-of-delivery flagged as forged. Customer OTP required."
    elif action == "SUBMIT_OTP":
        if otp_code == "849201":
            state["warden_action"] = "AUTO_CLEAR"
            state["trust_score"] = 85
            state["otp_verified"] = True
            state["last_message"] = "OTP 849201 verified. Consignment released."
        else:
            state["last_message"] = "Invalid OTP code entered."
    elif action == "TRIGGER_API_HARVEST":
        state["warden_action"] = "API_CREDENTIAL_REVOKED"
        state["trust_score"] = 10
        state["highest_velocity_kmh"] = 0.0
        state["last_message"] = "Credential revoked at API gateway. WAF blacklist applied."

    try:
        with open(BRIDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass
    return state

def update_warden_state(
    warden_action: str,
    trust_score: int,
    velocity: float,
    message: str,
    otp_verified: bool = False
):
    """Called by SOC command center orchestrator to synchronize policy decisions back to handset."""
    state = get_live_state()
    state["warden_action"] = warden_action
    state["trust_score"] = trust_score
    state["highest_velocity_kmh"] = velocity
    state["last_message"] = message
    if otp_verified:
        state["otp_verified"] = True
    try:
        with open(BRIDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass

def reset_live_state():
    """Resets the bridge to pristine default."""
    try:
        with open(BRIDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_STATE, f, indent=2)
    except Exception:
        pass
