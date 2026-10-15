"""
AegisNode - Sentinel Agent (Fast Telemetry & Access Scanner)
Monitors incoming GPS telemetry, telematics, and subcontractor API calls.
Detects physical impossibilities, short-hop teleportation, and fails closed on missing data.
Strict enterprise compliance - Zero Emojis.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from .osrm_service import haversine_distance_km
from .ledger import AuditLedger

def _parse_timestamp_seconds(ts_val: Any) -> float:
    """Safely normalizes string, float, or int ISO timestamps to UTC epoch seconds."""
    if isinstance(ts_val, (int, float)):
        return float(ts_val)
    if not isinstance(ts_val, str) or not ts_val.strip():
        return 0.0
    try:
        clean_ts = ts_val.strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_ts)
        return dt.timestamp()
    except Exception:
        return 0.0

class SentinelAgent:
    """First line of defense: high-throughput anomaly detector with fail-closed security."""

    def __init__(self, ledger: Optional[AuditLedger] = None):
        self.ledger = ledger

    def scan_telemetry(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scans courier delivery events for physical and metadata red flags."""
        # Handle API scraping scenario if present
        if "subcontractor_id" in scenario_data:
            return self._scan_api_access(scenario_data)

        events = scenario_data.get("events", [])
        flags: List[str] = []
        anomalies_detected = False
        highest_velocity_kmh = 0.0
        cell_tower_suspicion = False
        dwell_suspicion = False
        pod_flagged = False

        # Rule 1: Fail closed on zero telemetry events
        if not events or len(events) == 0:
            anomalies_detected = True
            flags.append("MISSING_TELEMETRY: Shipment contains zero telemetry events. Failing closed.")
            report = {
                "agent": "SentinelAgent",
                "status": "FLAGGED",
                "anomalies_detected": True,
                "primary_trigger": "MISSING_TELEMETRY",
                "shipment_id": scenario_data.get("shipment_id", "UNKNOWN"),
                "courier_id": scenario_data.get("courier_id", "UNKNOWN"),
                "highest_velocity_kmh": 0.0,
                "cell_tower_spoof_detected": False,
                "cell_tower_locked": False,
                "dwell_anomaly_detected": False,
                "pod_anomaly_detected": False,
                "flags": flags,
                "summary": "CRITICAL: Consignment has zero telematics breadcrumbs. Security quarantine engaged."
            }
            if self.ledger:
                self.ledger.record("SentinelAgent", "SCAN_TELEMETRY", report["shipment_id"], report)
            return report

        for i in range(1, len(events)):
            prev = events[i - 1]
            curr = events[i]

            t_prev_sec = _parse_timestamp_seconds(prev.get("timestamp"))
            t_curr_sec = _parse_timestamp_seconds(curr.get("timestamp"))
            delta_seconds = max(t_curr_sec - t_prev_sec, 0.5)
            delta_hours = delta_seconds / 3600.0

            loc1 = prev.get("location", {})
            loc2 = curr.get("location", {})

            # Rule 2: Fail closed on malformed location payloads
            if "lat" not in loc1 or "lon" not in loc1 or "lat" not in loc2 or "lon" not in loc2:
                anomalies_detected = True
                flags.append(f"MALFORMED_TELEMETRY: Checkpoint #{curr.get('sequence', i+1)} missing spatial coordinates.")
                continue

            lat1, lon1 = float(loc1["lat"]), float(loc1["lon"])
            lat2, lon2 = float(loc2["lat"]), float(loc2["lon"])
            dist_km = haversine_distance_km(lat1, lon1, lat2, lon2)

            speed_kmh = dist_km / delta_hours
            if speed_kmh > highest_velocity_kmh:
                highest_velocity_kmh = speed_kmh

            # Rule 3: Physical Velocity Anomaly (any jump > 0.05 km exceeding 110 km/h in urban Malaysia)
            if dist_km >= 0.05 and speed_kmh > 110.0:
                anomalies_detected = True
                flags.append(
                    f"IMPOSSIBLE VELOCITY: Traveled {dist_km:.2f} km in {delta_seconds:.0f}s "
                    f"(Calculated Speed: {speed_kmh:.0f} km/h)"
                )

            # Rule 4: Cell Tower Lock Anomaly (GPS moved >5km but connected tower ID did not change)
            cell1 = prev.get("cell_tower_id")
            cell2 = curr.get("cell_tower_id")
            if cell1 and cell2 and cell1 == cell2 and dist_km > 5.0:
                cell_tower_suspicion = True
                anomalies_detected = True
                flags.append(
                    f"CELL TOWER ANOMALY: GPS moved {dist_km:.1f} km but remained locked to Tower [{cell1}]. "
                    f"Indicates Android Mock Location software manipulation."
                )

            # Rule 5: Suspicious Dwell in Industrial area carrying high-value parcel
            if "Industrial" in loc2.get("label", "") and scenario_data.get("parcel_value_myr", 0) > 1000:
                dwell_suspicion = True
                flags.append(
                    f"HIGH-RISK DWELL: Stopped in {loc2.get('label', 'Industrial Zone')} carrying RM{scenario_data.get('parcel_value_myr', 0):.2f} cargo."
                )

            # Rule 6: POD Evidence verification
            pod = curr.get("pod_evidence")
            if pod and pod.get("photo_status") in ("SUSPICIOUS", "FORGED", "TEXTURE_DEFICIT", "REPLAY_ATTACK", "DECODE_FAILURE"):
                pod_flagged = True
                anomalies_detected = True
                flags.append(
                    f"POD INTEGRITY ALERT: Proof-of-Delivery flagged as {pod['photo_status']}."
                )

        # Primary trigger selection
        primary_trigger = "NONE"
        if "MISSING_TELEMETRY" in str(flags):
            primary_trigger = "MISSING_TELEMETRY"
        elif cell_tower_suspicion:
            primary_trigger = "MOCK_LOCATION_SPOOF"
        elif highest_velocity_kmh > 110.0:
            primary_trigger = "IMPOSSIBLE_VELOCITY"
        elif pod_flagged:
            primary_trigger = "POD_INTEGRITY_ALERT"
        elif dwell_suspicion:
            primary_trigger = "HIGH_RISK_DWELL"

        report = {
            "agent": "SentinelAgent",
            "status": "FLAGGED" if anomalies_detected else "CLEAR",
            "anomalies_detected": anomalies_detected,
            "primary_trigger": primary_trigger,
            "shipment_id": scenario_data.get("shipment_id", "UNKNOWN"),
            "courier_id": scenario_data.get("courier_id", "UNKNOWN"),
            "highest_velocity_kmh": round(highest_velocity_kmh, 1),
            "cell_tower_spoof_detected": cell_tower_suspicion,
            "cell_tower_locked": cell_tower_suspicion,
            "dwell_anomaly_detected": dwell_suspicion,
            "pod_anomaly_detected": pod_flagged,
            "flags": flags,
            "summary": (
                f"ANOMALY FLAGGED: {len(flags)} critical anomalies detected. Forwarding to Investigator Agent."
                if anomalies_detected
                else "CLEAR: Telemetry within normal physical and telematics parameters."
            )
        }

        if self.ledger:
            self.ledger.record(
                agent="SentinelAgent",
                action="SCAN_TELEMETRY",
                target_id=report["shipment_id"],
                details=report
            )

        return report

    def _scan_api_access(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scans subcontractor API traffic for anomalous access patterns dynamically."""
        events = scenario_data.get("events", [])
        flags: List[str] = []
        is_flagged = False

        if not events:
            return {
                "agent": "SentinelAgent",
                "status": "FLAGGED",
                "anomalies_detected": True,
                "shipment_id": scenario_data.get("subcontractor_id", "API-TARGET"),
                "flags": ["MISSING_ACCESS_LOGS: No gateway request telemetry provided."],
                "summary": "CRITICAL: Missing API access telemetry."
            }

        for ev in events:
            rate = ev.get("request_count_per_minute", 0)
            limit = ev.get("standard_rate_limit", 60)
            hour = ev.get("hour_of_day", 12)

            if rate > limit * 2:
                is_flagged = True
                flags.append(f"RATE ABUSE: {rate} req/min exceeds threshold ({limit} req/min)")
            if 0 <= hour <= 5:
                is_flagged = True
                flags.append(f"OUT-OF-HOURS ACCESS: Bulk manifest export attempted at {hour:02d}:00 AM")

        report = {
            "agent": "SentinelAgent",
            "status": "FLAGGED" if is_flagged else "CLEAR",
            "anomalies_detected": is_flagged,
            "shipment_id": scenario_data.get("subcontractor_id", "API-TARGET"),
            "flags": flags,
            "summary": "CRITICAL: Subcontractor API scraping attempt detected." if is_flagged else "CLEAR: API traffic nominal."
        }

        if self.ledger:
            self.ledger.record(
                agent="SentinelAgent",
                action="SCAN_API_ACCESS",
                target_id=report["shipment_id"],
                details=report
            )

        return report
