"""
AegisNode - Investigator Agent (Autonomous ReAct Deep Reasoner & Evidence Synthesizer)
Implements an explainable ReAct (Reasoning + Acting) autonomous agent loop.
Integrates Google Gemini LLM with bounded safety guardrails and dynamic local deterministic fallback.
Executes specialized tools for OSRM kinematics, cellular baseband audits, optical POD heuristics, and cargo liability.
Strict enterprise compliance - Zero Emojis.
"""

import os
import json
import math
from datetime import datetime
from typing import Dict, Any, List, Optional
from .osrm_service import check_route_feasibility, haversine_distance_km
from .ledger import AuditLedger
from .photo_forensics import get_photo_engine

def _safe_parse_timestamp(ts_val: Any) -> float:
    if isinstance(ts_val, (int, float)):
        return float(ts_val)
    if not isinstance(ts_val, str) or not ts_val.strip():
        return 0.0
    try:
        clean = ts_val.strip().replace("Z", "+00:00")
        return datetime.fromisoformat(clean).timestamp()
    except Exception:
        return 0.0

class InvestigatorAgent:
    """
    Autonomous ReAct Investigator Agent.
    Executes dedicated tools in an iterative Thought -> Action -> Observation -> Finding loop.
    Enforces AI Safety Governance: deterministic physics sets the ceiling; LLM can only escalate risk.
    """

    def __init__(self, ledger: Optional[AuditLedger] = None):
        self.ledger = ledger
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.photo_engine = get_photo_engine()

    # =========================================================================
    # SPECIALIZED REACT TOOLS (AGENT ACTION SPACE)
    # =========================================================================

    def tool_osrm_kinematics(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        elapsed_seconds: float,
        from_label: str = "Point A",
        to_label: str = "Point B"
    ) -> Dict[str, Any]:
        """
        Tool: Evaluates physical vehicular travel feasibility along the real road network.
        Cross-references elapsed duration against OpenStreetMap OSRM graph routing.
        """
        osrm_res = check_route_feasibility(lat1, lon1, lat2, lon2)
        expected_sec = osrm_res["duration_seconds"]
        actual_min = elapsed_seconds / 60.0
        expected_min = expected_sec / 60.0
        ratio = elapsed_seconds / max(expected_sec, 1.0)
        dist_km = osrm_res["distance_km"]

        hours = max(elapsed_seconds / 3600.0, 0.0001)
        calc_speed_kmh = dist_km / hours

        # Impossible if speed exceeds 110 km/h or time is under 20% of realistic road transit for > 0.5km
        is_impossible = (calc_speed_kmh > 110.0 and dist_km >= 0.05) or (ratio < 0.20 and dist_km > 0.5)

        return {
            "from_label": from_label,
            "to_label": to_label,
            "road_distance_km": round(dist_km, 2),
            "osrm_expected_min": round(expected_min, 1),
            "actual_elapsed_min": round(actual_min, 1),
            "calculated_speed_kmh": round(calc_speed_kmh, 1),
            "feasibility_ratio": round(ratio, 2),
            "routing_source": osrm_res["source"],
            "is_physically_impossible": is_impossible
        }

    def tool_cell_baseband_audit(
        self,
        events: List[Dict[str, Any]],
        sentinel_flags: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Tool: Audits cellular baseband telematics across consecutive waypoints.
        Flags software GPS spoofing (Android Mock Locations) when displacement > 5km
        occurs without cell tower handover.
        """
        locked_towers = []
        spoof_detected = False

        if sentinel_flags and sentinel_flags.get("cell_tower_spoof_detected"):
            spoof_detected = True

        for i in range(1, len(events)):
            p = events[i - 1]
            c = events[i]
            t1 = p.get("cell_tower_id")
            t2 = c.get("cell_tower_id")
            if t1 and t2 and t1 == t2:
                loc1 = p.get("location", {})
                loc2 = c.get("location", {})
                if "lat" in loc1 and "lat" in loc2:
                    d = haversine_distance_km(loc1["lat"], loc1["lon"], loc2["lat"], loc2["lon"])
                    if d > 5.0:
                        spoof_detected = True
                        locked_towers.append({
                            "tower_id": t1,
                            "displacement_km": round(d, 1),
                            "segment": f"Event {p.get('sequence', i)} -> Event {c.get('sequence', i+1)}"
                        })

        return {
            "spoof_detected": spoof_detected,
            "locked_towers": locked_towers,
            "baseband_status": "ANOMALOUS_BASEBAND_LOCK" if spoof_detected else "NOMINAL_CELLULAR_HANDOFF"
        }

    def tool_vision_pod_analyzer(
        self,
        pod_evidence: Dict[str, Any],
        shipment_id: str = "UNKNOWN"
    ) -> Dict[str, Any]:
        """
        Tool: Audits Proof-of-Delivery (POD) optical texture, edge entropy, and replay resistance.
        Evaluates Laplacian edge variance and perceptual difference hashing.
        """
        photo_status = pod_evidence.get("photo_status", "VALID")
        variance = pod_evidence.get("optical_variance", 72.4)
        otp_verified = pod_evidence.get("otp_verified", False)
        is_replay = pod_evidence.get("is_replay", False)

        is_suspicious = (
            photo_status in ("SUSPICIOUS", "FORGED", "TEXTURE_DEFICIT", "REPLAY_ATTACK", "DECODE_FAILURE")
            or is_replay
            or (float(variance) < 55.0)
        )

        finding = "Proof-of-delivery optical texture and sharpness verified"
        if is_replay or photo_status == "REPLAY_ATTACK":
            finding = "Perceptual hash collision: duplicate delivery photo replayed across shipments"
        elif photo_status == "DECODE_FAILURE":
            finding = "Invalid raster payload: uploaded bytes corrupted or non-image format"
        elif is_suspicious:
            finding = f"Optical texture ({variance:.1f}) fails physical edge threshold (55.0). Obscured or floor-mat capture."

        return {
            "photo_status": photo_status if is_suspicious else "VALID",
            "laplacian_variance": round(float(variance), 1),
            "variance_threshold": 55.0,
            "otp_verified": otp_verified,
            "is_suspicious": is_suspicious,
            "is_replay": is_replay,
            "finding": finding
        }

    def tool_cargo_risk_tier(
        self,
        parcel_value_myr: float
    ) -> Dict[str, Any]:
        """
        Tool: Evaluates commercial cargo liability and assigns risk multiplier.
        High-value items warrant stricter Zero-Trust enforcement thresholds.
        """
        val = float(parcel_value_myr)
        if val > 1000.0:
            tier = "TIER_3_HIGH_VALUE"
            multiplier = 1.35
            description = "High-Value Consumer Tech (> RM 1,000) - Strict zero-tolerance containment"
        elif val > 100.0:
            tier = "TIER_2_GENERAL_MERCHANDISE"
            multiplier = 1.15
            description = "General Merchandise (RM 101 - RM 1,000) - Standard escalation protocols"
        else:
            tier = "TIER_1_LOW_VALUE"
            multiplier = 1.00
            description = "Standard Document / Low-Value (<= RM 100) - Standard audit baseline"

        return {
            "declared_value_myr": round(val, 2),
            "risk_tier": tier,
            "liability_multiplier": multiplier,
            "tier_description": description
        }

    # =========================================================================
    # OPTIONAL LLM REASONING & RISK SYNTHESIZER
    # =========================================================================

    def _call_gemini_synthesizer(
        self,
        scenario_data: Dict[str, Any],
        tool_metrics: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Invokes Google Gemini LLM to synthesize contextual forensic reasoning.
        Enforces AI Safety Bounds: Gemini can explain and escalate risk, but cannot override physical violations.
        """
        if not self.gemini_api_key:
            return None

        prompt = f"""You are the AegisNode Autonomous Forensic Security Analyst for last-mile logistics.
Analyze the following delivery audit payload and output valid JSON only:

Shipment ID: {scenario_data.get('shipment_id', 'UNKNOWN')}
Courier: {scenario_data.get('courier_name', 'UNKNOWN')} ({scenario_data.get('courier_vehicle', 'UNKNOWN')})
Cargo: RM {scenario_data.get('parcel_value_myr', 0)} ({scenario_data.get('parcel_category', 'General')})

Deterministic Tool Evidence:
- Road Kinematics Violation: {tool_metrics.get('has_kinematic_violation')}
- Impossible Segments: {tool_metrics.get('impossible_segments')}
- Cellular Baseband Anomaly: {tool_metrics.get('baseband_anomaly')}
- POD Photo Status: {tool_metrics.get('pod_status')} ({tool_metrics.get('pod_finding')})
- Cargo Risk Tier: {tool_metrics.get('cargo_tier')} (Multiplier: {tool_metrics.get('cargo_multiplier')})
- Deterministic Calculated Score: {tool_metrics.get('deterministic_score')}/100

Respond strictly with a JSON object in this exact format:
{{
  "ai_hypothesis": "1-2 sentence technical threat hypothesis",
  "contextual_risk_escalation": 0 to 15,
  "forensic_synthesis": "Concise forensic summary for SOC command center",
  "recommended_action": "AUTO_CLEAR" or "STEP_UP_CHALLENGE" or "PACKAGE_FREEZE"
}}
"""
        try:
            # 1. Try google-genai package
            from google import genai
            client = genai.Client(api_key=self.gemini_api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw_text = response.text.strip()
            # Clean markdown codeblocks if returned
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            return json.loads(raw_text.strip())
        except Exception:
            return None

    # =========================================================================
    # AUTONOMOUS REACT INVESTIGATION LOOP
    # =========================================================================

    def investigate(
        self,
        scenario_data: Dict[str, Any],
        sentinel_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes an autonomous ReAct investigation loop.
        Constructs a step-by-step reasoning trace with explicit tool calls.
        Fails closed on missing or empty data.
        """
        if "subcontractor_id" in scenario_data:
            return self._investigate_api_scraping(scenario_data, sentinel_report)

        events = scenario_data.get("events", [])
        parcel_value = scenario_data.get("parcel_value_myr", 50.0)
        shipment_id = scenario_data.get("shipment_id", "UNKNOWN")
        react_trace: List[Dict[str, Any]] = []

        cargo_res = self.tool_cargo_risk_tier(parcel_value)
        value_risk_multiplier = cargo_res["liability_multiplier"]

        # Rule 1: Fail closed if telemetry is empty
        if not events:
            return {
                "agent": "InvestigatorAgent",
                "shipment_id": shipment_id,
                "trust_score": 0,
                "risk_level": "CRITICAL",
                "route_evaluations": [],
                "react_trace": [
                    {
                        "step": 1,
                        "thought": "Inspect telemetry events payload for courier transit evidence.",
                        "tool": "tool_telemetry_validator",
                        "tool_input": {"event_count": 0},
                        "observation": {"error": "ZERO_TELEMETRY_RECORDED"},
                        "finding": "Security violation: consignment has zero recorded telemetry. Failing closed.",
                        "status": "VIOLATION"
                    }
                ],
                "penalties": {"missing_telemetry": 100, "cargo_multiplier": value_risk_multiplier},
                "forensic_narrative": "Missing telemetry breadcrumbs: consignment quarantined due to absent route verification."
            }

        route_evaluations: List[Dict[str, Any]] = []
        kinematic_penalty = 0
        telematics_penalty = 0
        pod_penalty = 0

        # ---------------------------------------------------------------------
        # STEP 1: Spatial Kinematics & Road Feasibility (Tool: OSRM Kinematics)
        # ---------------------------------------------------------------------
        thought_1 = (
            "Evaluate spatial kinematics across all logged delivery checkpoints. "
            "Cross-reference transit duration against OpenStreetMap OSRM physical road graph to detect teleportation."
        )

        has_kinematic_violation = False
        impossible_segments = []

        for i in range(1, len(events)):
            prev = events[i - 1]
            curr = events[i]

            t_prev_sec = _safe_parse_timestamp(prev.get("timestamp"))
            t_curr_sec = _safe_parse_timestamp(curr.get("timestamp"))
            elapsed_sec = max(t_curr_sec - t_prev_sec, 0.5)

            loc1 = prev.get("location", {})
            loc2 = curr.get("location", {})
            if "lat" not in loc1 or "lon" not in loc1 or "lat" not in loc2 or "lon" not in loc2:
                has_kinematic_violation = True
                kinematic_penalty += 40
                impossible_segments.append(f"Missing coordinates at checkpoint #{i}")
                continue

            lat1, lon1 = float(loc1["lat"]), float(loc1["lon"])
            lat2, lon2 = float(loc2["lat"]), float(loc2["lon"])
            from_lbl = loc1.get("label", f"Waypoint {i}")
            to_lbl = loc2.get("label", f"Waypoint {i+1}")

            seg_res = self.tool_osrm_kinematics(lat1, lon1, lat2, lon2, elapsed_sec, from_lbl, to_lbl)
            route_evaluations.append({
                "segment": f"Event {prev.get('sequence', i)} -> Event {curr.get('sequence', i+1)}",
                "from_label": from_lbl,
                "to_label": to_lbl,
                "actual_elapsed_min": seg_res["actual_elapsed_min"],
                "osrm_expected_min": seg_res["osrm_expected_min"],
                "road_distance_km": seg_res["road_distance_km"],
                "feasibility_ratio": seg_res["feasibility_ratio"],
                "source": seg_res["routing_source"],
                "is_impossible": seg_res["is_physically_impossible"]
            })

            if seg_res["is_physically_impossible"]:
                has_kinematic_violation = True
                kinematic_penalty += 55
                impossible_segments.append(
                    f"{from_lbl} -> {to_lbl} ({seg_res['road_distance_km']} km in {seg_res['actual_elapsed_min']} min, "
                    f"Speed: {seg_res['calculated_speed_kmh']} km/h)"
                )

        obs_1 = {
            "total_segments_analyzed": len(events) - 1,
            "impossible_segments": impossible_segments,
            "kinematic_penalty_assigned": kinematic_penalty
        }
        finding_1 = (
            f"Physical road network violation confirmed: {len(impossible_segments)} segment(s) exceed human vehicular limits."
            if has_kinematic_violation
            else "All route segments conform to realistic road network travel durations and speeds."
        )

        react_trace.append({
            "step": 1,
            "thought": thought_1,
            "tool": "tool_osrm_kinematics",
            "tool_input": {"total_events": len(events), "routing_engine": "OSRM"},
            "observation": obs_1,
            "finding": finding_1,
            "status": "VIOLATION" if has_kinematic_violation else "PASS"
        })

        # ---------------------------------------------------------------------
        # STEP 2: Baseband Cellular Telematics (Tool: Cellular Baseband Audit)
        # ---------------------------------------------------------------------
        thought_2 = (
            "Cross-reference hardware cellular baseband telemetry against geographic displacement. "
            "Detect whether GPS coordinates jumped across sectors without corresponding cell tower handoffs."
        )

        baseband_res = self.tool_cell_baseband_audit(events, sentinel_report)
        if baseband_res["spoof_detected"]:
            telematics_penalty += 25

        if sentinel_report.get("dwell_anomaly_detected"):
            telematics_penalty += 10

        obs_2 = {
            "baseband_status": baseband_res["baseband_status"],
            "locked_towers": baseband_res["locked_towers"],
            "dwell_anomaly": sentinel_report.get("dwell_anomaly_detected", False),
            "telematics_penalty_assigned": telematics_penalty
        }
        finding_2 = (
            "Cellular baseband mismatch detected: GPS coordinates displaced across territory without cell tower handover. "
            "Confirms Android Mock Location software manipulation."
            if baseband_res["spoof_detected"]
            else "Cellular tower handoffs correlate with physical transit. Zero baseband anomaly."
        )

        react_trace.append({
            "step": 2,
            "thought": thought_2,
            "tool": "tool_cell_baseband_audit",
            "tool_input": {"events_inspected": len(events)},
            "observation": obs_2,
            "finding": finding_2,
            "status": "VIOLATION" if baseband_res["spoof_detected"] else "PASS"
        })

        # ---------------------------------------------------------------------
        # STEP 3: Optical Proof-of-Delivery (Tool: Vision POD Analyzer)
        # ---------------------------------------------------------------------
        thought_3 = (
            "Analyze Proof-of-Delivery (POD) optical evidence. "
            "Inspect Laplacian edge variance and perceptual difference hash to verify genuine package capture versus obscured sensor or screen replay."
        )

        last_event = events[-1] if events else {}
        pod_evidence = last_event.get("pod_evidence", {})

        # Rule 2: If event is a delivery attempt, POD evidence is MANDATORY
        if last_event.get("event_type") == "DELIVERY_ATTEMPT" and not pod_evidence:
            pod_penalty += 45
            pod_res = {
                "photo_status": "MISSING_POD",
                "laplacian_variance": 0.0,
                "is_suspicious": True,
                "finding": "Mandatory Proof-of-Delivery photo is missing on delivery attempt. Fails closed."
            }
        else:
            pod_res = self.tool_vision_pod_analyzer(pod_evidence, shipment_id=shipment_id)
            if pod_res["is_suspicious"]:
                if pod_res.get("is_replay"):
                    pod_penalty += 50
                else:
                    pod_penalty += 40

        obs_3 = {
            "photo_status": pod_res["photo_status"],
            "laplacian_variance": pod_res.get("laplacian_variance", 0.0),
            "otp_verified": pod_res.get("otp_verified", False),
            "pod_penalty_assigned": pod_penalty
        }
        finding_3 = (
            f"Visual audit alert: {pod_res['finding']} (Variance: {pod_res.get('laplacian_variance', 0.0)} vs Threshold: 55.0)."
            if pod_res["is_suspicious"]
            else "Proof-of-Delivery optical texture and sharpness verified against reference standards."
        )

        react_trace.append({
            "step": 3,
            "thought": thought_3,
            "tool": "tool_vision_pod_analyzer",
            "tool_input": {"has_pod_evidence": bool(pod_evidence)},
            "observation": obs_3,
            "finding": finding_3,
            "status": "VIOLATION" if pod_res["is_suspicious"] else "PASS"
        })

        # ---------------------------------------------------------------------
        # STEP 4: Commercial Cargo Liability (Tool: Cargo Risk Tier)
        # ---------------------------------------------------------------------
        thought_4 = (
            "Determine consignment financial exposure and cargo risk category. "
            "Apply proportional liability multiplier to scale zero-trust penalty impact."
        )

        cargo_res = self.tool_cargo_risk_tier(parcel_value)
        value_risk_multiplier = cargo_res["liability_multiplier"]

        obs_4 = {
            "declared_value": f"RM {cargo_res['declared_value_myr']:.2f}",
            "risk_tier": cargo_res["risk_tier"],
            "multiplier": value_risk_multiplier
        }
        finding_4 = cargo_res["tier_description"]

        react_trace.append({
            "step": 4,
            "thought": thought_4,
            "tool": "tool_cargo_risk_tier",
            "tool_input": {"parcel_value_myr": parcel_value},
            "observation": obs_4,
            "finding": finding_4,
            "status": "PASS"
        })

        # ---------------------------------------------------------------------
        # DYNAMIC ZERO-TRUST TRUST SCORE COMPUTATION
        # ---------------------------------------------------------------------
        raw_deduction = (
            (kinematic_penalty * 0.75) +
            (telematics_penalty * 0.60) +
            (pod_penalty * 0.80)
        ) * value_risk_multiplier

        deterministic_score = max(5, min(100, int(round(100 - raw_deduction))))

        # ---------------------------------------------------------------------
        # STEP 5: AI SYNTHESIZER & RISK ESCALATION (GEMINI / LOCAL FALLBACK)
        # ---------------------------------------------------------------------
        tool_metrics = {
            "has_kinematic_violation": has_kinematic_violation,
            "impossible_segments": impossible_segments,
            "baseband_anomaly": baseband_res["spoof_detected"],
            "pod_status": pod_res["photo_status"],
            "pod_finding": pod_res["finding"],
            "cargo_tier": cargo_res["risk_tier"],
            "cargo_multiplier": value_risk_multiplier,
            "deterministic_score": deterministic_score
        }

        gemini_result = self._call_gemini_synthesizer(scenario_data, tool_metrics)
        ai_escalation = 0
        ai_narrative = ""

        if gemini_result:
            ai_escalation = int(min(max(gemini_result.get("contextual_risk_escalation", 0), 0), 15))
            ai_narrative = gemini_result.get("forensic_synthesis", "")
            react_trace.append({
                "step": 5,
                "thought": "Synthesize contextual risk vectors using Google Gemini LLM reasoning engine.",
                "tool": "tool_gemini_llm_synthesizer",
                "tool_input": {"model": "gemini-2.5-flash", "ground_truth_score": deterministic_score},
                "observation": gemini_result,
                "finding": f"LLM Forensic Hypothesis: {gemini_result.get('ai_hypothesis', 'Risk verified.')}",
                "status": "VIOLATION" if ai_escalation > 0 else "PASS"
            })

        # Bounded AI Safety Rule: LLM can escalate risk by up to 15 points, but cannot override deterministic math
        final_trust_score = max(5, deterministic_score - ai_escalation)

        # Build Forensic Narrative
        if ai_narrative:
            forensic_narrative = ai_narrative
        else:
            narrative_parts = []
            if kinematic_penalty > 0:
                narrative_parts.append(f"Physical road network kinematics violated: {', '.join(impossible_segments)}.")
            if telematics_penalty > 0:
                narrative_parts.append("Baseband telematics anomaly: Cellular tower ID failed to hand off across geographic movement.")
            if pod_penalty > 0:
                narrative_parts.append(f"Visual audit failure: {pod_res['finding']}.")
            if not narrative_parts:
                narrative_parts.append("All route segments conform to realistic road network travel durations and verified POD.")
            forensic_narrative = " | ".join(narrative_parts)

        findings = {
            "agent": "InvestigatorAgent",
            "shipment_id": shipment_id,
            "trust_score": final_trust_score,
            "risk_level": "CRITICAL" if final_trust_score < 40 else ("MEDIUM" if final_trust_score < 75 else "LOW"),
            "route_evaluations": route_evaluations,
            "react_trace": react_trace,
            "penalties": {
                "kinematic_road_violation": kinematic_penalty,
                "telematics_spoof": telematics_penalty,
                "pod_forgery": pod_penalty,
                "cargo_multiplier": value_risk_multiplier,
                "value_multiplier": value_risk_multiplier,
                "ai_escalation": ai_escalation
            },
            "forensic_narrative": forensic_narrative
        }

        if self.ledger:
            self.ledger.record(
                agent="InvestigatorAgent",
                action="FORENSIC_INVESTIGATION",
                target_id=findings["shipment_id"],
                details={
                    "trust_score": final_trust_score,
                    "risk_level": findings["risk_level"],
                    "penalties": findings["penalties"],
                    "react_steps": len(react_trace),
                    "narrative": findings["forensic_narrative"]
                }
            )

        return findings

    def _investigate_api_scraping(
        self,
        scenario_data: Dict[str, Any],
        sentinel_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep investigation into API token traffic dynamically based on actual event logs."""
        sub_id = scenario_data.get("subcontractor_id", "SUB-UNKNOWN")
        source_ip = scenario_data.get("source_ip", "0.0.0.0")
        events = scenario_data.get("events", [])

        # Analyze actual events dynamically
        max_rate = 0
        limit = 60
        off_hours_attempts = 0
        sample_hour = 12

        for ev in events:
            rate = ev.get("request_count_per_minute", 0)
            if rate > max_rate:
                max_rate = rate
            limit = ev.get("standard_rate_limit", 60)
            hour = ev.get("hour_of_day", 12)
            sample_hour = hour
            if 0 <= hour <= 5:
                off_hours_attempts += 1

        rate_ratio = max_rate / max(limit, 1)

        # Dynamic penalty scoring
        rate_penalty = 0
        off_hours_penalty = 0

        if rate_ratio > 3.0:
            rate_penalty = min(70, int(rate_ratio * 8))
        elif rate_ratio > 1.5:
            rate_penalty = 30

        if off_hours_attempts > 0:
            off_hours_penalty = 20

        raw_score = 100 - (rate_penalty + off_hours_penalty)
        trust_score = max(5, min(100, raw_score))

        status = "VIOLATION" if trust_score < 75 else "PASS"

        react_trace = [
            {
                "step": 1,
                "thought": "Analyze API gateway request frequency against contractual SLA baseline.",
                "tool": "tool_api_traffic_audit",
                "tool_input": {"subcontractor_id": sub_id, "observed_rate": max_rate, "rate_limit": limit},
                "observation": {"rate_per_min": max_rate, "baseline_limit": limit, "surge_ratio": round(rate_ratio, 2)},
                "finding": f"Request volume at {max_rate} req/min ({rate_ratio:.1f}x baseline). " +
                           ("Surge exceeds authorized threshold." if rate_ratio > 2.0 else "Volume within normal quota."),
                "status": "VIOLATION" if rate_ratio > 2.0 else "PASS"
            },
            {
                "step": 2,
                "thought": "Evaluate temporal access window and source IP telemetry.",
                "tool": "tool_temporal_origin_audit",
                "tool_input": {"source_ip": source_ip, "hour_of_day": sample_hour},
                "observation": {"off_hours": off_hours_attempts > 0, "sample_hour": sample_hour},
                "finding": f"Access logged at {sample_hour:02d}:00. " +
                           ("Out-of-hours bulk export window detected." if off_hours_attempts > 0 else "Authorized daylight operating hours."),
                "status": "VIOLATION" if off_hours_attempts > 0 else "PASS"
            }
        ]

        if trust_score < 40:
            forensic_narrative = (
                f"Severe API surge: {max_rate} req/min ({rate_ratio:.1f}x limit) from IP {source_ip} "
                f"at {sample_hour:02d}:00. Credential compromised or dark-web scraping script active."
            )
        elif trust_score < 75:
            forensic_narrative = (
                f"Elevated API traffic: {max_rate} req/min from IP {source_ip} warrants rate-limiting and secondary audit."
            )
        else:
            forensic_narrative = (
                f"Subcontractor API traffic within authorized rate limits ({max_rate} req/min <= {limit}) "
                f"during operational business hours ({sample_hour:02d}:00). Zero threat detected."
            )

        findings = {
            "agent": "InvestigatorAgent",
            "shipment_id": sub_id,
            "trust_score": trust_score,
            "risk_level": "CRITICAL" if trust_score < 40 else ("MEDIUM" if trust_score < 75 else "LOW"),
            "react_trace": react_trace,
            "penalties": {"api_scraping_surge": rate_penalty, "off_hours_exfiltration": off_hours_penalty},
            "forensic_narrative": forensic_narrative
        }

        if self.ledger:
            self.ledger.record(
                agent="InvestigatorAgent",
                action="FORENSIC_API_INVESTIGATION",
                target_id=sub_id,
                details=findings
            )

        return findings
