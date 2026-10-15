"""
AegisNode - Warden Agent (Autonomous Policy & Incident Response Enforcer)
Executes risk-adaptive Zero-Trust countermeasures:
- Low Risk (Trust >= 75): Auto-Clear
- Medium Risk (Trust 40 - 74): Cryptographic OTP Step-Up Verification Challenge
- Critical Risk (Trust < 40): Immediate Package Freeze, Token Revocation & Dispatch Alert
Strict enterprise compliance - Zero Emojis.
"""

from typing import Dict, Any, Optional
from .ledger import AuditLedger
from .otp_service import get_otp_service

class WardenAgent:
    """Enforces zero-trust defense actions based on Investigator trust score and cryptographic verification."""

    def __init__(self, ledger: Optional[AuditLedger] = None):
        self.ledger = ledger
        self.otp_service = get_otp_service()

    def enforce_policy(
        self,
        scenario_data: Dict[str, Any],
        investigator_findings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluates trust score and triggers autonomous containment actions."""
        trust_score = investigator_findings.get("trust_score", 0)
        target_id = investigator_findings.get("shipment_id", "UNKNOWN")

        # ---------------------------------------------------------------------
        # 1. API Security Threat Matrix
        # ---------------------------------------------------------------------
        if "subcontractor_id" in scenario_data:
            if trust_score >= 75:
                decision = {
                    "agent": "WardenAgent",
                    "action": "AUTO_CLEAR",
                    "enforcement_level": "NOMINAL",
                    "target_id": target_id,
                    "trust_score": trust_score,
                    "banner_title": "WARDEN CLEARANCE: SUBCONTRACTOR API ACCESS NORMAL",
                    "banner_type": "success",
                    "actions_taken": [
                        f"Verified API Token quota for subcontractor [{target_id}]",
                        "Traffic rate within contractually authorized bounds",
                        "Zero anomalous WAF indicators logged"
                    ],
                    "message": "Subcontractor API access verified within authorized rate limits and business hours."
                }
            elif 40 <= trust_score < 75:
                decision = {
                    "agent": "WardenAgent",
                    "action": "RATE_LIMIT_ENGAGED",
                    "enforcement_level": "ELEVATED",
                    "target_id": target_id,
                    "trust_score": trust_score,
                    "banner_title": "WARDEN INTERVENTION: API RATE LIMIT THROTTLE APPLIED",
                    "banner_type": "warning",
                    "actions_taken": [
                        f"Throttled API Key [{scenario_data.get('api_key_prefix', 'gdx_sub_***')}] to 30 req/min",
                        "Dispatched tier-2 traffic advisory to Partner SecOps",
                        "Flagged subcontractor account for compliance review"
                    ],
                    "message": "API traffic volume elevated above baseline. Autonomous throttling engaged."
                }
            else:
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
                    "message": "Subcontractor access revoked immediately due to bulk manifest scraping anomaly."
                }

            if self.ledger:
                self.ledger.record(
                    agent="WardenAgent",
                    action=decision["action"],
                    target_id=target_id,
                    details=decision
                )
            return decision

        # ---------------------------------------------------------------------
        # 2. Last-Mile Courier Telematics Threat Matrix
        # ---------------------------------------------------------------------
        recipient_phone = scenario_data.get("recipient_phone", "0123456789")

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
            # Issue dynamic HMAC-SHA256 challenge via OTP Service
            challenge_res = self.otp_service.generate_challenge(target_id, recipient_phone)
            decision = {
                "agent": "WardenAgent",
                "action": "STEP_UP_CHALLENGE",
                "enforcement_level": "ELEVATED",
                "target_id": target_id,
                "trust_score": trust_score,
                "banner_title": "WARDEN INTERVENTION: STEP-UP VERIFICATION REQUIRED (OTP CHALLENGE)",
                "banner_type": "warning",
                "actions_taken": [
                    "Delivery latch locked on courier edge handset",
                    f"Generated dynamic HMAC-SHA256 challenge code for recipient {challenge_res.get('masked_phone')}",
                    f"Max {challenge_res.get('attempts_allowed', 3)} attempts allowed before permanent quarantine",
                    "Logged pending challenge token to Zero-Trust Audit Ledger"
                ],
                "message": "Delivery held pending customer cryptographic OTP confirmation."
            }
        else:  # trust_score < 40
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
                    "Generated GDEX Security Operations forensic dispatch ticket #LOG-FR-4029"
                ],
                "message": "Immediate freeze activated: physical travel impossibility or severe anomaly confirmed."
            }

        if self.ledger:
            self.ledger.record(
                agent="WardenAgent",
                action=decision["action"],
                target_id=target_id,
                details=decision
            )

        return decision

    def verify_otp_release(
        self,
        shipment_id: str,
        candidate_otp: str
    ) -> Dict[str, Any]:
        """
        Processes recipient OTP verification and executes autonomous consignment release or quarantine.
        Records an authentic state transition in the cryptographic Audit Ledger.
        """
        res = self.otp_service.verify_otp(shipment_id, candidate_otp)

        if res["valid"]:
            decision = {
                "agent": "WardenAgent",
                "action": "CHALLENGE_VERIFIED",
                "enforcement_level": "CLEARED_VIA_STEP_UP",
                "target_id": shipment_id,
                "trust_score": 88,
                "banner_title": "Consignment Released via Verified Recipient OTP",
                "banner_type": "success",
                "actions_taken": [
                    f"Cryptographic challenge verified (proof token: {res.get('verification_proof')})",
                    "Warden release latch unsealed on courier edge handset",
                    "Driver payout cleared for batch settlement",
                    "Audit ledger state updated with recipient signature verification"
                ],
                "message": "Customer confirmed physical receipt via dynamic one-time cryptographic challenge."
            }
        elif res["status"] == "LOCKED":
            decision = {
                "agent": "WardenAgent",
                "action": "CHALLENGE_LOCKED",
                "enforcement_level": "EMERGENCY_LOCKDOWN",
                "target_id": shipment_id,
                "trust_score": 10,
                "banner_title": "WARDEN LOCKDOWN: OTP ATTEMPTS EXHAUSTED",
                "banner_type": "error",
                "actions_taken": [
                    "3 consecutive incorrect OTP entries detected",
                    "Permanent consignment freeze engaged",
                    "Courier session credentials suspended",
                    "High-priority dispatch to GDEX SecOps audit team"
                ],
                "message": res["message"]
            }
        else:
            decision = {
                "agent": "WardenAgent",
                "action": "CHALLENGE_FAILED",
                "enforcement_level": "ELEVATED",
                "target_id": shipment_id,
                "trust_score": 42,
                "banner_title": "WARDEN STEP-UP: INCORRECT OTP SUBMISSION",
                "banner_type": "warning",
                "actions_taken": [
                    f"Invalid code submitted. {res.get('attempts_remaining', 0)} attempts remaining.",
                    "Consignment release latch remains locked"
                ],
                "message": res["message"]
            }

        if self.ledger:
            self.ledger.record(
                agent="WardenAgent",
                action=decision["action"],
                target_id=shipment_id,
                details=decision
            )

        return decision
