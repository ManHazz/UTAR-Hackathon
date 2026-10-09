"""
Unit and integration tests for AegisNode Multi-Agent system
"""

import json
from pathlib import Path
from aegisnode.agents.ledger import AuditLedger, AuditBlock
from aegisnode.agents.osrm_service import check_route_feasibility, haversine_distance_km
from aegisnode.agents.orchestrator import AegisNodeOrchestrator

DATA_DIR = Path(__file__).parent.parent / "data"

def test_ledger_cryptographic_integrity():
    ledger = AuditLedger()
    ledger.record("AgentA", "TEST_ACTION", "ID-1", {"val": 123})
    ledger.record("AgentB", "TEST_ACTION2", "ID-2", {"val": 456})

    verification = ledger.verify_integrity()
    assert verification["valid"] is True
    assert verification["total_blocks"] == 3  # Genesis + 2

def test_haversine_distance():
    # Shah Alam Central Hub to PJ SS2 (approx 10-15 km)
    dist = haversine_distance_km(3.0738, 101.5385, 3.1186, 101.6214)
    assert 9.0 < dist < 15.0

def test_osrm_route_feasibility_fallback():
    # Shah Alam Section 23 to Menara PJX
    res = check_route_feasibility(3.0450, 101.5200, 3.1032, 101.6445)
    assert res["distance_km"] > 10.0
    assert res["duration_minutes"] > 15.0
    assert res["source"] in ("LIVE_OSRM", "PREBAKED_CACHE", "PHYSICS_ESTIMATION")

def test_normal_delivery_pipeline():
    with open(DATA_DIR / "normal_delivery.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    orchestrator = AegisNodeOrchestrator()
    result = orchestrator.process_shipment(data)

    assert result["sentinel"]["status"] == "CLEAR"
    assert result["investigator"]["trust_score"] >= 75
    assert result["warden"]["action"] == "AUTO_CLEAR"
    assert result["ledger_status"]["valid"] is True

def test_gps_spoof_detection_pipeline():
    with open(DATA_DIR / "fraud_gps_spoof.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    orchestrator = AegisNodeOrchestrator()
    result = orchestrator.process_shipment(data)

    assert result["sentinel"]["status"] == "FLAGGED"
    assert result["sentinel"]["cell_tower_spoof_detected"] is True
    assert result["investigator"]["trust_score"] < 40
    assert result["warden"]["action"] == "PACKAGE_FREEZE"
    assert "WARDEN LOCKDOWN" in result["warden"]["banner_title"]
    assert result["ledger_status"]["valid"] is True

def test_pod_spoof_detection_pipeline():
    with open(DATA_DIR / "fraud_pod_spoof.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    orchestrator = AegisNodeOrchestrator()
    result = orchestrator.process_shipment(data)

    assert result["sentinel"]["pod_anomaly_detected"] is True
    assert result["investigator"]["trust_score"] < 75
    assert result["warden"]["action"] == "STEP_UP_CHALLENGE"

def test_api_scraping_detection_pipeline():
    with open(DATA_DIR / "fraud_api_scraping.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    orchestrator = AegisNodeOrchestrator()
    result = orchestrator.process_shipment(data)

    assert result["sentinel"]["status"] == "FLAGGED"
    assert result["warden"]["action"] == "API_CREDENTIAL_REVOKED"

def test_tiered_cargo_multipliers():
    from aegisnode.agents.investigator_agent import InvestigatorAgent
    investigator = InvestigatorAgent()

    # Tier 1: Low-value doc
    res_low = investigator.investigate(
        {"events": [], "parcel_value_myr": 50.0},
        {"cell_tower_spoof_detected": False}
    )
    assert res_low["penalties"]["cargo_multiplier"] == 1.00

    # Tier 2: General merchandise
    res_med = investigator.investigate(
        {"events": [], "parcel_value_myr": 450.0},
        {"cell_tower_spoof_detected": False}
    )
    assert res_med["penalties"]["cargo_multiplier"] == 1.15

    # Tier 3: High-value consumer electronics
    res_high = investigator.investigate(
        {"events": [], "parcel_value_myr": 2500.0},
        {"cell_tower_spoof_detected": False}
    )
    assert res_high["penalties"]["cargo_multiplier"] == 1.35

def test_sentinel_json_contract():
    from aegisnode.agents.sentinel_agent import SentinelAgent
    sentinel = SentinelAgent()

    with open(DATA_DIR / "fraud_gps_spoof.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    report = sentinel.scan_telemetry(data)
    assert "primary_trigger" in report
    assert report["primary_trigger"] == "MOCK_LOCATION_SPOOF"
    assert "cell_tower_locked" in report
    assert report["cell_tower_locked"] is True

def test_ledger_tamper_rejection():
    ledger = AuditLedger()
    b1 = ledger.record("Agent1", "ACTION_1", "ID-1", {"val": 100})
    b2 = ledger.record("Agent2", "ACTION_2", "ID-2", {"val": 200})

    # Legitimate state is valid
    assert ledger.verify_integrity()["valid"] is True

    # Tamper with block #1
    tampered_block = AuditBlock(
        index=b1.index,
        timestamp=b1.timestamp,
        agent=b1.agent,
        action=b1.action,
        target_id=b1.target_id,
        details={"val": 9999}, # Malicious modification
        prev_hash=b1.prev_hash,
        block_hash=b1.block_hash
    )
    ledger.chain[1] = tampered_block

    # Integrity verification must catch tampering
    verification = ledger.verify_integrity()
    assert verification["valid"] is False
    assert verification["tampered_at_index"] == 1

