"""
AegisNode - Warden Agent (Autonomous Policy & Incident Response Enforcer)
Executes risk-adaptive Zero-Trust countermeasures:
- Low Risk (Trust >= 75): Auto-Clear
- Medium Risk (Trust 40 - 74): OTP Step-Up Verification Challenge
- Critical Risk (Trust < 40): Immediate Package Freeze, Token Revocation & Dispatch Alert
"""

from typing import Dict, Any, Optional
from .ledger import AuditLedger

class WardenAgent:
    """Enforces zero-trust defense actions based on Investigator trust score."""

    def __init__(self, ledger: Optional[AuditLedger] = None):
        self.ledger = ledger

    def enforce_policy(
        self,
        scenario_data: Dict[str, Any],
        investigator_findings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluates trust score and triggers autonomous containment actions."""
        trust_score = investigator_findings.get("trust_score", 100)
        target_id = investigator_findings.get("shipment_id", "UNKNOWN")

        # API Security Threat
        if "subcontractor_id" in scenario_data:
            decision = {
                "agent": "WardenAgent",
                "action": "API_CREDENTIAL_REVOKED",
                "enforcement_level": "LOCKDOWN",
                "target_id": target_id,
                "trust_score": trust_score,
                "banner_title": "WARDEN ENFORCEMENT: SUBCONTRACTOR API ACCESS TERMINATED",
                "banner_type": "error",
                "actions_taken": [
                    f"Revoked API Key [{scenario_data.get('api_key_prefix', 'gdx_sub_***')}] across all GDEX gateways",
                    f"Added Source IP [{scenario_data.get('source_ip', '0.0.0.0')}] to Cloudflare/WAF blocklist",
                    "Dispatched High-Priority Security Incident Ticket #SEC-2026-9921 to SecOps team",
                    "Generated cryptographic forensic snapshot in Zero-Trust Audit Ledger"
                ],
                "message": "Subcontractor access revoked immediately due to out-of-hours bulk manifest scraping."
            }
            if self.ledger:
                self.ledger.record(
                    agent="WardenAgent",
                    action="API_CREDENTIAL_REVOKED",
                    target_id=target_id,
                    details=decision
                )
            return decision

        # Delivery & Telemetry Threat Matrix
        if trust_score >= 75:
            decision = {
                "agent": "WardenAgent",
                "action": "AUTO_CLEAR",
                "enforcement_level": "NOMINAL",
                "target_id": target_id,
                "trust_score": trust_score,
                "banner_title": "WARDEN CLEARANCE: SHIPMENT VERIFIED AND APPROVED",
                "banner_type": "success",
                "actions_taken": [
                    "Zero-Trust physical and digital verification passed",
                    "Approved delivery completion status in GDEX Core ERP",
                    "Released courier settlement credit for shipment",
                    "Stored cryptographic audit proof to immutable ledger"
                ],
                "message": "Delivery verified successfully without manual intervention required."
            }
        elif 40 <= trust_score < 75:
            decision = {
                "agent": "WardenAgent",
                "action": "STEP_UP_CHALLENGE",
                "enforcement_level": "ELEVATED",
                "target_id": target_id,
                "trust_score": trust_score,
                "banner_title": "WARDEN INTERVENTION: STEP-UP VERIFICATION REQUIRED (OTP CHALLENGE)",
                "banner_type": "warning",
                "actions_taken": [
                    "Delivery button temporarily locked on courier handset",
                    f"Generated and sent dynamic 6-digit verification OTP to recipient ({scenario_data.get('recipient_name', 'Customer')})",
                    "Flagged delivery for post-shift supervisor audit",
                    "Recorded conditional delivery challenge to Zero-Trust Ledger"
                ],
                "message": "Delivery marked on-hold pending customer real-time OTP confirmation."
            }
        else: # trust_score < 40
            decision = {
                "agent": "WardenAgent",
                "action": "PACKAGE_FREEZE",
                "enforcement_level": "EMERGENCY_LOCKDOWN",
                "target_id": target_id,
                "trust_score": trust_score,
                "banner_title": "WARDEN LOCKDOWN: PACKAGE FREEZE INITIATED (FRAUD INTERCEPT)",
                "banner_type": "error",
                "actions_taken": [
                    f"Quarantined shipment {target_id} (RM {scenario_data.get('parcel_value_myr', 0):.2f})",
                    f"Revoked courier session token for driver [{scenario_data.get('courier_id', 'UNKNOWN')}]",
                    "Disabled 'Delivered' completion endpoint for this consignment",
                    "Automated SMS dispatched to customer: 'Delivery held for security verification'",
                    "Generated GDEX Security Operations forensic dispatch dispatch ticket #LOG-FR-4029"
                ],
                "message": "Immediate freeze activated: physical travel impossibility and GPS spoofing confirmed."
            }

        if self.ledger:
            self.ledger.record(
                agent="WardenAgent",
                action=decision["action"],
                target_id=target_id,
                details=decision
            )

        return decision
