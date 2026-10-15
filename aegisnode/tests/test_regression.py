"""
AegisNode - Security and Fail-Closed Regression Test Suite
Validates all vulnerability fixes raised during security and AI governance audit:
1. Telemetry fail-closed on zero events
2. Short-hop velocity detection (< 3 km at impossible speeds)
3. Corrupted image bytes and non-raster uploads fail closed
4. Perceptual difference hashing (dHash) detects photo replay attacks
5. Dynamic HMAC-SHA256 OTP control rejects arbitrary digits and enforces lockout
6. Tamper-evident ledger non-repudiation with HMAC digital signatures and rollback defense
7. Dynamic API scraping analysis (evaluates real traffic vs hardcoded strings)
8. Safe timezone normalization across ISO timestamps

Strict enterprise compliance - Zero Emojis.
"""

import os
import time
import pytest
from datetime import datetime, timezone
from pathlib import Path

from aegisnode.agents.sentinel_agent import SentinelAgent
from aegisnode.agents.investigator_agent import InvestigatorAgent
from aegisnode.agents.warden_agent import WardenAgent
from aegisnode.agents.orchestrator import AegisNodeOrchestrator
from aegisnode.agents.ledger import AuditLedger, AuditBlock
from aegisnode.agents.otp_service import OTPService
from aegisnode.agents.photo_forensics import PhotoForensicsEngine

# -----------------------------------------------------------------------------
# 1. FAIL-CLOSED TELEMETRY AUDIT
# -----------------------------------------------------------------------------

def test_missing_telemetry_fails_closed():
    """Shipment with zero telemetry events must fail closed (Trust 0, FLAGGED)."""
    sentinel = SentinelAgent()
    investigator = InvestigatorAgent()
    warden = WardenAgent()

    empty_scenario = {
        "shipment_id": "GDX-TEST-ZERO-01",
        "events": [],
        "parcel_value_myr": 500.0
    }

    s_rep = sentinel.scan_telemetry(empty_scenario)
    assert s_rep["anomalies_detected"] is True
    assert s_rep["primary_trigger"] == "MISSING_TELEMETRY"

    inv_rep = investigator.investigate(empty_scenario, s_rep)
    assert inv_rep["trust_score"] == 0
    assert inv_rep["risk_level"] == "CRITICAL"

    decision = warden.enforce_policy(empty_scenario, inv_rep)
    assert decision["action"] in ("PACKAGE_FREEZE", "STEP_UP_CHALLENGE")

# -----------------------------------------------------------------------------
# 2. SHORT-HOP VELOCITY DETECTION (< 3 KM AT HIGH SPEEDS)
# -----------------------------------------------------------------------------

def test_short_hop_teleportation_detected():
    """
    Moving 1.5 km in 20 seconds equates to 270 km/h.
    The Sentinel must flag this as an impossible velocity anomaly.
    """
    sentinel = SentinelAgent()

    # Lat 4.3850 to 4.3985 is approx 1.5 km
    short_hop_scenario = {
        "shipment_id": "GDX-TEST-HOP-01",
        "events": [
            {
                "sequence": 1,
                "timestamp": "2026-10-15T14:00:00",
                "location": {"lat": 4.385000, "lon": 100.978000, "label": "Start"},
                "speed_kmh": 30.0
            },
            {
                "sequence": 2,
                "timestamp": "2026-10-15T14:00:20",  # 20 seconds later
                "location": {"lat": 4.398500, "lon": 100.978000, "label": "Jump"},
                "speed_kmh": 30.0
            }
        ]
    }

    report = sentinel.scan_telemetry(short_hop_scenario)
    assert report["anomalies_detected"] is True
    assert report["highest_velocity_kmh"] > 150.0

# -----------------------------------------------------------------------------
# 3. PHOTO FORENSICS FAIL-CLOSED ON BAD BYTES
# -----------------------------------------------------------------------------

def test_corrupted_image_bytes_fail_closed():
    """Corrupted garbage bytes uploaded as a POD photo must fail closed as FORGED."""
    engine = PhotoForensicsEngine()
    garbage_bytes = b"NOT_A_VALID_JPEG_OR_PNG_HEADER_JUST_RANDOM_GARBAGE_BYTES_1234567890"

    res = engine.analyze_photo_bytes(garbage_bytes, shipment_id="GDX-TEST-BAD-01")
    assert res["status"] in ("FORGED", "DECODE_FAILURE")
    assert res["variance"] == 0.0

def test_blank_or_flat_image_texture_deficit():
    """Synthetic solid color image with zero edge variance must flag TEXTURE_DEFICIT."""
    engine = PhotoForensicsEngine()
    # 200x200 solid gray synthetic PNG bytes
    import numpy as np
    import cv2
    flat_img = np.full((200, 200, 3), 128, dtype=np.uint8)
    _, flat_bytes = cv2.imencode(".jpg", flat_img)

    res = engine.analyze_photo_bytes(flat_bytes.tobytes(), shipment_id="GDX-TEST-FLAT-01")
    assert res["status"] in ("FORGED", "TEXTURE_DEFICIT")
    assert res["variance"] < 5.0

# -----------------------------------------------------------------------------
# 4. PERCEPTUAL DIFFERENCE HASHING (REPLAY ATTACK RESISTANCE)
# -----------------------------------------------------------------------------

def test_perceptual_hash_replay_detection():
    """Submitting the exact same photo across two shipments must flag REPLAY_ATTACK."""
    import numpy as np
    import cv2
    engine = PhotoForensicsEngine(registry_path=Path("aegisnode/tests/scratch_photo_registry.json"))

    # Generate synthetic textured test image with high edge variance
    np.random.seed(42)
    img = np.random.randint(50, 220, (200, 200, 3), dtype=np.uint8)
    cv2.putText(img, "PARCEL-123-AUTHENTIC", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    _, valid_bytes = cv2.imencode(".jpg", img)
    raw = valid_bytes.tobytes()

    # First delivery: should succeed
    res1 = engine.analyze_photo_bytes(raw, shipment_id="GDX-SHP-ORIG-01")
    assert res1["status"] in ("VERIFIED", "VALID")
    assert res1["is_replay"] is False

    # Second delivery with reused photo: must trigger REPLAY_ATTACK
    res2 = engine.analyze_photo_bytes(raw, shipment_id="GDX-SHP-REUSED-02")
    assert res2["is_replay"] is True
    assert res2["status"] == "REPLAY_ATTACK"

    # Cleanup test scratch registry
    if engine.registry_path and engine.registry_path.exists():
        try:
            os.remove(engine.registry_path)
        except OSError:
            pass

# -----------------------------------------------------------------------------
# 5. DYNAMIC HMAC-SHA256 OTP WITH LOCKOUT
# -----------------------------------------------------------------------------

def test_insecure_otp_rejection_and_lockout():
    """Arbitrary 6-digit codes (e.g. 000000) must fail; 3 failures trigger lockout."""
    otp_service = OTPService()
    shipment_id = "GDX-OTP-REG-01"

    # Issue dynamic challenge
    otp_service.generate_challenge(shipment_id, recipient_phone="0128910423")
    active_code = otp_service.get_active_plain_otp_for_sms_simulation(shipment_id)
    assert active_code is not None
    assert len(active_code) == 6

    # Attempt 1: Insecure 000000 rejected
    v1 = otp_service.verify_otp(shipment_id, "000000")
    assert v1["valid"] is False
    assert v1["attempts_remaining"] == 2

    # Attempt 2: Another wrong code rejected
    v2 = otp_service.verify_otp(shipment_id, "123456")
    assert v2["valid"] is False
    assert v2["attempts_remaining"] == 1

    # Attempt 3: Third wrong code triggers lockout
    v3 = otp_service.verify_otp(shipment_id, "999999")
    assert v3["valid"] is False
    assert v3["status"] == "LOCKED"

    # Subsequent attempt with correct code must now fail due to LOCKOUT
    v_locked = otp_service.verify_otp(shipment_id, active_code)
    assert v_locked["valid"] is False
    assert v_locked["status"] == "LOCKED"

def test_dynamic_hmac_otp_success():
    """Verifying with the generated HMAC passcode succeeds and marks challenge VERIFIED."""
    otp_service = OTPService()
    shipment_id = "GDX-OTP-SUCCESS-01"

    otp_service.generate_challenge(shipment_id, recipient_phone="0128910423")
    active_code = otp_service.get_active_plain_otp_for_sms_simulation(shipment_id)

    res = otp_service.verify_otp(shipment_id, active_code)
    assert res["valid"] is True
    assert res["status"] == "VERIFIED"

# -----------------------------------------------------------------------------
# 6. TAMPER-EVIDENT HMAC SIGNED LEDGER & ROLLBACK DEFENSE
# -----------------------------------------------------------------------------

def test_ledger_hmac_signature_detects_recomputed_hash():
    """
    If an attacker modifies a block and recalculates SHA-256 hashes down the chain,
    the HMAC digital signature check must still fail because the attacker lacks the secret key.
    """
    ledger = AuditLedger()
    b1 = ledger.record("AgentA", "ACTION_1", "SHIP-01", {"score": 95})
    b2 = ledger.record("AgentB", "ACTION_2", "SHIP-01", {"verdict": "CLEAR"})

    assert ledger.verify_integrity()["valid"] is True

    # Attacker modifies b1 payload and recalculates its SHA-256 hash
    forged_details = {"score": 10}
    forged_hash = AuditLedger._calculate_hash(
        index=b1.index,
        timestamp=b1.timestamp,
        agent=b1.agent,
        action=b1.action,
        target_id=b1.target_id,
        details=forged_details,
        prev_hash=b1.prev_hash
    )
    # The attacker attaches forged block with their recalculation but without a valid HMAC signature
    tampered_block = AuditBlock(
        index=b1.index,
        timestamp=b1.timestamp,
        agent=b1.agent,
        action=b1.action,
        target_id=b1.target_id,
        details=forged_details,
        prev_hash=b1.prev_hash,
        block_hash=forged_hash,
        signature="FORGED_HMAC_SIGNATURE_BYTES"
    )
    ledger.chain[1] = tampered_block

    verification = ledger.verify_integrity()
    assert verification["valid"] is False
    assert "signature invalid" in verification["reason"]

def test_ledger_rollback_detection():
    """Truncating or deleting blocks from the chain must trigger rollback failure."""
    ledger = AuditLedger()
    ledger.record("AgentA", "ACTION_1", "SHIP-01", {"step": 1})
    ledger.record("AgentB", "ACTION_2", "SHIP-01", {"step": 2})
    ledger.record("AgentC", "ACTION_3", "SHIP-01", {"step": 3})

    expected_blocks = len(ledger.chain)  # 4 blocks (Genesis + 3)

    # Malicious actor drops the last block
    ledger.chain.pop()

    verification = ledger.verify_integrity(expected_total_blocks=expected_blocks)
    assert verification["valid"] is False
    assert "Rollback detected" in verification["reason"]

def test_ledger_idempotency_on_reruns():
    """Identical agent recordings on Streamlit page reruns must not create duplicate blocks."""
    ledger = AuditLedger()
    initial_count = len(ledger.chain)

    # First call
    b1 = ledger.record("AgentX", "SCAN", "SHIP-RERUN", {"status": "NOMINAL"})
    assert len(ledger.chain) == initial_count + 1

    # Second identical call (simulating Streamlit rerun)
    b2 = ledger.record("AgentX", "SCAN", "SHIP-RERUN", {"status": "NOMINAL"})
    assert len(ledger.chain) == initial_count + 1
    assert b1 == b2

# -----------------------------------------------------------------------------
# 7. DYNAMIC API SCRAPING TRAFFIC EVALUATION
# -----------------------------------------------------------------------------

def test_dynamic_api_evaluation_harmless_traffic():
    """Harmless API traffic (10 req/min at 2 PM) must not be flagged as Tor exit node scraping."""
    sentinel = SentinelAgent()
    investigator = InvestigatorAgent()

    harmless_api_payload = {
        "subcontractor_id": "SUB-NORMAL-01",
        "api_partner_name": "SwiftHaul Logistics",
        "events": [
            {
                "request_count_per_minute": 10,
                "standard_rate_limit": 120,
                "hour_of_day": 14,
                "endpoint": "/api/v2/shipment/status"
            }
        ]
    }

    s_rep = sentinel.scan_telemetry(harmless_api_payload)
    assert s_rep["anomalies_detected"] is False

    inv_rep = investigator.investigate(harmless_api_payload, s_rep)
    assert inv_rep["trust_score"] >= 80
    assert inv_rep["risk_level"] in ("LOW", "NOMINAL")
    # Must not contain canned Tor string
    assert "Tor exit node" not in inv_rep.get("forensic_narrative", "")

def test_dynamic_api_evaluation_surge_traffic():
    """Abnormal API traffic exceeding rate limits during night hours must trigger revocation."""
    sentinel = SentinelAgent()
    investigator = InvestigatorAgent()

    surge_api_payload = {
        "subcontractor_id": "SUB-SCRAPE-99",
        "api_partner_name": "Shadow Haul",
        "events": [
            {
                "request_count_per_minute": 650,
                "standard_rate_limit": 60,
                "hour_of_day": 3,
                "endpoint": "/api/v2/shipment/status"
            }
        ]
    }

    s_rep = sentinel.scan_telemetry(surge_api_payload)
    assert s_rep["anomalies_detected"] is True

    inv_rep = investigator.investigate(surge_api_payload, s_rep)
    assert inv_rep["trust_score"] <= 25
    assert inv_rep["risk_level"] == "CRITICAL"

# -----------------------------------------------------------------------------
# 8. SAFE TIMEZONE NORMALIZATION
# -----------------------------------------------------------------------------

def test_mixed_timezone_timestamps_do_not_crash():
    """Mixed timezone ISO strings and naive timestamps must parse safely without TypeError."""
    sentinel = SentinelAgent()

    mixed_tz_scenario = {
        "shipment_id": "GDX-TZ-01",
        "events": [
            {
                "sequence": 1,
                "timestamp": "2026-10-15T14:00:00Z",  # UTC ISO
                "location": {"lat": 4.3850, "lon": 100.9780},
                "speed_kmh": 25.0
            },
            {
                "sequence": 2,
                "timestamp": "2026-10-15T22:05:00+08:00",  # +08:00 ISO
                "location": {"lat": 4.3870, "lon": 100.9750},
                "speed_kmh": 28.0
            },
            {
                "sequence": 3,
                "timestamp": "2026-10-15T14:10:00",  # Naive ISO
                "location": {"lat": 4.3890, "lon": 100.9720},
                "speed_kmh": 30.0
            }
        ]
    }

    report = sentinel.scan_telemetry(mixed_tz_scenario)
    assert report is not None
    assert "highest_velocity_kmh" in report
