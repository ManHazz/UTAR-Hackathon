"""
AegisNode - Sentinel Agent (Fast Telemetry & Access Scanner)
Monitors incoming GPS telemetry, telematics, and subcontractor API calls.
Detects physical impossibilities and telemetry spoofing indicators.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from .osrm_service import haversine_distance_km
from .ledger import AuditLedger

class SentinelAgent:
    """First line of defense: high-throughput anomaly detector."""

    def __init__(self, ledger: Optional[AuditLedger] = None):
        self.ledger = ledger

    def scan_telemetry(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scans courier delivery events for physical and metadata red flags."""
        events = scenario_data.get("events", [])
        flags: List[str] = []
        anomalies_detected = False
        highest_velocity_kmh = 0.0
        cell_tower_suspicion = False
        dwell_suspicion = False
        pod_flagged = False

        # Handle API scraping scenario if present
        if "subcontractor_id" in scenario_data:
            return self._scan_api_access(scenario_data)

        for i in range(1, len(events)):
            prev = events[i - 1]
            curr = events[i]

            t_prev = datetime.fromisoformat(prev["timestamp"])
            t_curr = datetime.fromisoformat(curr["timestamp"])
            delta_seconds = max((t_curr - t_prev).total_seconds(), 1.0)
            delta_hours = delta_seconds / 3600.0

            lat1, lon1 = prev["location"]["lat"], prev["location"]["lon"]
            lat2, lon2 = curr["location"]["lat"], curr["location"]["lon"]
            dist_km = haversine_distance_km(lat1, lon1, lat2, lon2)

            speed_kmh = dist_km / delta_hours
            if speed_kmh > highest_velocity_kmh:
                highest_velocity_kmh = speed_kmh

            # Rule 1: Impossible Physical Velocity (>120 km/h in urban Selangor/KL)
            if speed_kmh > 120.0 and dist_km > 3.0:
                anomalies_detected = True
                flags.append(
                    f"IMPOSSIBLE VELOCITY: Traveled {dist_km:.1f} km in {delta_seconds/60:.1f} min "
                    f"(Calculated Speed: {speed_kmh:.0f} km/h)"
                )

            # Rule 2: Cell Tower Discrepancy (GPS moved >5km but connected cell tower ID did not change)
            cell1 = prev.get("cell_tower_id")
            cell2 = curr.get("cell_tower_id")
            if cell1 and cell2 and cell1 == cell2 and dist_km > 5.0:
                cell_tower_suspicion = True
                anomalies_detected = True
                flags.append(
                    f"CELL TOWER ANOMALY: GPS moved {dist_km:.1f} km but remained locked to Tower [{cell1}]. "
                    f"Strong indicator of GPS Mock Location / Software Spoofing."
                )

            # Rule 3: Suspicious Dwell in Industrial/Off-Route area with high-value parcel
            if "Industrial" in curr.get("location", {}).get("label", "") and scenario_data.get("parcel_value_myr", 0) > 1000:
                dwell_suspicion = True
                flags.append(
                    f"HIGH-RISK DWELL: Stopped in {curr['location']['label']} carrying RM{scenario_data['parcel_value_myr']:.2f} electronics."
                )

            # Rule 4: POD Evidence verification flag
            pod = curr.get("pod_evidence")
            if pod and pod.get("photo_status") in ("SUSPICIOUS", "FORGED"):
                pod_flagged = True
                anomalies_detected = True
                flags.append(
                    f"POD INTEGRITY ALERT: Proof-of-Delivery flagged as {pod['photo_status']} ({pod.get('photo_label')})."
                )

        report = {
            "agent": "SentinelAgent",
            "status": "FLAGGED" if anomalies_detected else "CLEAR",
            "anomalies_detected": anomalies_detected,
            "shipment_id": scenario_data.get("shipment_id", "UNKNOWN"),
            "courier_id": scenario_data.get("courier_id", "UNKNOWN"),
            "highest_velocity_kmh": round(highest_velocity_kmh, 1),
            "cell_tower_spoof_detected": cell_tower_suspicion,
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
        """Scans subcontractor API traffic for anomalous access patterns."""
        events = scenario_data.get("events", [])
        flags: List[str] = []
        is_flagged = False

        for ev in events:
            rate = ev.get("request_count_per_minute", 0)
            limit = ev.get("standard_rate_limit", 60)
            hour = ev.get("hour_of_day", 12)

            if rate > limit * 3:
                is_flagged = True
                flags.append(f"RATE ABUSE: {rate} req/min exceeds threshold ({limit} req/min)")
            if hour >= 0 and hour <= 5:
                is_flagged = True
                flags.append(f"OUT-OF-HOURS ACCESS: Bulk manifest export attempted at 0{hour}:00 AM")

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
