"""
Unit and integration tests for AegisNode Multi-Agent system
"""

import json
from pathlib import Path
from aegisnode.agents.ledger import AuditLedger
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
