"""
AegisNode - Multi-Agent Orchestrator
Coordinates Sentinel, Investigator, and Warden agents with the Cryptographic Zero-Trust Audit Ledger.
Strict enterprise compliance - Zero Emojis.
"""

from typing import Dict, Any, Optional
from .ledger import AuditLedger
from .sentinel_agent import SentinelAgent
from .investigator_agent import InvestigatorAgent
from .warden_agent import WardenAgent
from .otp_service import get_otp_service

class AegisNodeOrchestrator:
    """Manages the lifecycle of an autonomous Zero-Trust investigation and step-up verification."""

    def __init__(self, ledger: Optional[AuditLedger] = None):
        self.ledger = ledger if ledger is not None else AuditLedger()
        self.sentinel = SentinelAgent(self.ledger)
        self.investigator = InvestigatorAgent(self.ledger)
        self.warden = WardenAgent(self.ledger)
        self.otp_service = get_otp_service()

    def process_shipment(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs the full 3-agent Zero-Trust verification pipeline:
        1. Sentinel scans telemetry pings / access logs
        2. Investigator deep-checks OSRM routing and multimodal evidence
        3. Warden applies risk-adaptive containment
        """
        # Step 1: Sentinel Scan
        sentinel_result = self.sentinel.scan_telemetry(scenario_data)

        # Step 2: Investigator Forensic Analysis
        investigator_result = self.investigator.investigate(scenario_data, sentinel_result)

        # Step 3: Warden Enforcement
        warden_result = self.warden.enforce_policy(scenario_data, investigator_result)

        # Step 4: Validate Ledger Integrity
        ledger_status = self.ledger.verify_integrity()

        return {
            "scenario": scenario_data,
            "sentinel": sentinel_result,
            "investigator": investigator_result,
            "warden": warden_result,
            "ledger_status": ledger_status,
            "audit_trail": self.ledger.get_records()
        }

    def verify_shipment_otp(self, shipment_id: str, candidate_otp: str) -> Dict[str, Any]:
        """
        Processes recipient step-up challenge through the Warden agent and updates audit ledger.
        Enforces authentic cryptographic verification without frontend bypasses.
        """
        warden_decision = self.warden.verify_otp_release(shipment_id, candidate_otp)
        ledger_status = self.ledger.verify_integrity()
        return {
            "shipment_id": shipment_id,
            "warden": warden_decision,
            "ledger_status": ledger_status,
            "audit_trail": self.ledger.get_records()
        }
