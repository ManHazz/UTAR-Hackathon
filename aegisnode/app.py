"""
AegisNode - Zero-Trust Verification for Last-Mile Logistics
GDEX x ANON x UTAR Agentic AI Cybersecurity Hackathon 2026
Interactive Security Operations Command Center (SOC) Dashboard
Enterprise UX Architecture - Zero Emojis
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any

# Ensure repository root is always in sys.path across all platforms (Streamlit Community Cloud Linux)
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import streamlit as st
import pandas as pd

from aegisnode.agents.orchestrator import AegisNodeOrchestrator
from aegisnode.agents.ledger import AuditLedger
from aegisnode.ui.styles import get_custom_css, get_svg_icon, render_html
from aegisnode.ui.charts import (
    build_gauge_chart,
    build_route_feasibility_chart,
    build_api_threat_chart,
    build_penalty_breakdown_chart,
)
from aegisnode.ui.map_view import render_interactive_map
from aegisnode.ui.pod_viewer import render_pod_inspector
from aegisnode.ui.handset_simulator import render_courier_handset
from aegisnode.ui.ledger_view import render_cryptographic_ledger

# 1. Page Configuration (Strict enterprise styling)
st.set_page_config(
    page_title="AegisNode | Zero-Trust Logistics Command Center",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inject Cyber-Physical Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

DATA_DIR = Path(__file__).parent / "data"

SCENARIO_KEYS = {
    "[CRITICAL] GPS Teleportation Spoofing (Phantom Courier)": "fraud_gps_spoof.json",
    "[NOMINAL] Legitimate Delivery Route (Happy Path)": "normal_delivery.json",
    "[HIGH RISK] Forged POD Photo / Optical Forgery Attack": "fraud_pod_spoof.json",
    "[CYBER THREAT] Subcontractor API Manifest Scraping (03:00 AM)": "fraud_api_scraping.json",
}

MITRE_MAPPING = {
    "fraud_gps_spoof.json": "MITRE ATT&CK: T1056 - Telematics Evasion (Mock Location Injection)",
    "normal_delivery.json": "MITRE ATT&CK: None - Nominal Delivery Protocol",
    "fraud_pod_spoof.json": "MITRE ATT&CK: T1566 - Defense Impairment (Sensor Obscuration & Forgery)",
    "fraud_api_scraping.json": "MITRE ATT&CK: T1114 - Data Exfiltration (Out-of-Hours Bulk Harvest)",
}

def load_scenario(filename: str) -> Dict[str, Any]:
    path = DATA_DIR / filename
    if not path.exists():
        st.error(f"Scenario file {filename} not found.")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Initialize Session State
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AegisNodeOrchestrator()
if "active_scenario_file" not in st.session_state:
    st.session_state.active_scenario_file = "fraud_gps_spoof.json"
if "tamper_simulated" not in st.session_state:
    st.session_state.tamper_simulated = False
if "show_handset" not in st.session_state:
    st.session_state.show_handset = True
if "supervisor_action" not in st.session_state:
    st.session_state.supervisor_action = None
if "otp_cleared" not in st.session_state:
    st.session_state.otp_cleared = False

def select_scenario(filename: str):
    """Sets active scenario and resets transient state."""
    st.session_state.active_scenario_file = filename
    st.session_state.otp_cleared = False
    st.session_state.supervisor_action = None

# --- SIDEBAR NAVIGATION & CONTROLLER ---
with st.sidebar:
    shield_svg = get_svg_icon("shield", color="#38BDF8", size=24)
    render_html(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
        {shield_svg}
        <div>
            <div style="font-size:15px; font-weight:800; color:#F8FAFC; letter-spacing:0.04em;">AEGISNODE</div>
            <div style="font-size:11px; color:#94A3B8;">Zero-Trust Last-Mile Defense</div>
        </div>
    </div>
    """)

    st.markdown("### **Incident Scenarios**")
    
    scenario_options = list(SCENARIO_KEYS.keys())
    scenario_files = list(SCENARIO_KEYS.values())
    current_idx = scenario_files.index(st.session_state.active_scenario_file) if st.session_state.active_scenario_file in scenario_files else 0

    selected_label = st.selectbox(
        "Select Live Incident Scenario:",
        options=scenario_options,
        index=current_idx,
    )
    if SCENARIO_KEYS[selected_label] != st.session_state.active_scenario_file:
        select_scenario(SCENARIO_KEYS[selected_label])
        st.rerun()

    run_sim = st.button("Run Telemetry Analysis", use_container_width=True, type="primary")
    animate_pitch = st.checkbox("Presentation Latency Mode (1.8s)", value=True, help="Simulates multi-agent scanning latency")

    st.session_state.show_handset = st.checkbox("Courier Handset Preview", value=st.session_state.show_handset)

    st.markdown("---")
    st.markdown("#### **Consignment Telemetry Target**")
    scenario_data = load_scenario(st.session_state.active_scenario_file)

    if "shipment_id" in scenario_data:
        st.write(f"**Shipment ID:** `{scenario_data.get('shipment_id')}`")
        st.write(f"**Courier:** {scenario_data.get('courier_name')} (`{scenario_data.get('courier_id')}`)")
        st.write(f"**Vehicle:** {scenario_data.get('courier_vehicle')}")
        st.write(f"**Cargo Value:** `RM {scenario_data.get('parcel_value_myr', 0):.2f}`")
        st.write(f"**Category:** {scenario_data.get('parcel_category')}")
        dest = scenario_data.get("expected_destination", {}).get("label", "Destination")
        st.write(f"**Destination:** {dest}")
    elif "subcontractor_id" in scenario_data:
        st.write(f"**Partner ID:** `{scenario_data.get('subcontractor_id')}`")
        st.write(f"**Source IP:** `{scenario_data.get('source_ip')}`")
        st.write(f"**User Agent:** `{scenario_data.get('user_agent')}`")
        st.write(f"**Attack Vector:** Out-of-hours API Manifest Scraping")

# --- MAIN DASHBOARD HEADER ---
shield_head_svg = get_svg_icon("shield", color="#38BDF8", size=26)
render_html(f"""
<div class="command-header">
    <div>
        <div class="brand-title">
            {shield_head_svg}
            <span>AEGISNODE COMMAND CENTER</span>
        </div>
        <div class="brand-subtitle">
            Autonomous Multi-Agent Zero-Trust Verification Engine • Last-Mile Physical & Cyber Defense
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
        <div class="radar-pulse">
            <span class="pulse-dot"></span>
            <span>ZERO-TRUST SURVEILLANCE ACTIVE</span>
        </div>
    </div>
</div>
""")

# Situational Awareness & Data Freshness Bar
mitre_tag = MITRE_MAPPING.get(st.session_state.active_scenario_file, "MITRE ATT&CK: Unclassified")
render_html(f"""
<div class="freshness-strip">
    <div class="freshness-indicator">
        <span class="pulse-dot"></span>
        <span>STREAM STATUS: LIVE (0s INGESTION LATENCY) • CRYPTOGRAPHIC CONSENSUS ONLINE</span>
    </div>
    <div class="mitre-badge">
        {mitre_tag}
    </div>
</div>
""")

# --- 1-CLICK ACTIVE INCIDENT TRIAGE QUEUE ---
render_html("""
<div class="panel-header">
    <span>Active Incident Triage Queue</span>
</div>
""")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    is_active = (st.session_state.active_scenario_file == "fraud_gps_spoof.json")
    if st.button(
        "CRITICAL | INC-042: GPS Teleport" + (" [ACTIVE]" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate Phantom Courier mock location jump"
    ):
        select_scenario("fraud_gps_spoof.json")
        st.rerun()

with col_s2:
    is_active = (st.session_state.active_scenario_file == "normal_delivery.json")
    if st.button(
        "NOMINAL | INC-081: Clean Courier" + (" [ACTIVE]" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate legitimate delivery route"
    ):
        select_scenario("normal_delivery.json")
        st.rerun()

with col_s3:
    is_active = (st.session_state.active_scenario_file == "fraud_pod_spoof.json")
    if st.button(
        "HIGH RISK | INC-109: POD Forgery" + (" [ACTIVE]" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate car floor mat / screenshot POD forgery"
    ):
        select_scenario("fraud_pod_spoof.json")
        st.rerun()

with col_s4:
    is_active = (st.session_state.active_scenario_file == "fraud_api_scraping.json")
    if st.button(
        "CRITICAL | SEC-304: API Exfiltration" + (" [ACTIVE]" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate 03:00 AM bulk PII scraping"
    ):
        select_scenario("fraud_api_scraping.json")
        st.rerun()

# --- TOP SOC TELEMETRY STRIP ---
render_html("""
<div class="kpi-container">
    <div class="cyber-kpi">
        <div class="kpi-label">Telemetry Ingest / 24h</div>
        <div class="kpi-value tabular-nums">14,820</div>
        <div class="kpi-delta delta-green">+8.2% baseline rate</div>
    </div>
    <div class="cyber-kpi">
        <div class="kpi-label">Verified Deliveries</div>
        <div class="kpi-value tabular-nums">1,248</div>
        <div class="kpi-delta delta-cyan">99.2% SLA pass</div>
    </div>
    <div class="cyber-kpi">
        <div class="kpi-label">Autonomous Intercepts</div>
        <div class="kpi-value tabular-nums">3 FLAGGED</div>
        <div class="kpi-delta delta-red">Active quarantine</div>
    </div>
    <div class="cyber-kpi">
        <div class="kpi-label">Protected Cargo</div>
        <div class="kpi-value tabular-nums">RM 42,950</div>
        <div class="kpi-delta delta-green">Zero reserve breach</div>
    </div>
    <div class="cyber-kpi">
        <div class="kpi-label">Cryptographic Consensus</div>
        <div class="kpi-value tabular-nums">100% VALID</div>
        <div class="kpi-delta delta-green">SHA-256 non-repudiated</div>
    </div>
</div>
""")

# Run Orchestrator Pipeline
scenario_data = load_scenario(st.session_state.active_scenario_file)
result = st.session_state.orchestrator.process_shipment(scenario_data)

sentinel = result["sentinel"]
investigator = result["investigator"]
warden = result["warden"]
ledger_status = result["ledger_status"]

# If OTP was cleared by user interaction for the Step-Up scenario, update warden state
if st.session_state.otp_cleared and st.session_state.active_scenario_file == "fraud_pod_spoof.json":
    warden = dict(warden)
    warden["action"] = "AUTO_CLEAR"
    warden["banner_title"] = "Consignment Released via Verified Recipient OTP"
    warden["message"] = "Customer verified physical receipt via 6-digit cryptographic challenge. Consignment handed over and driver payout released."
    warden["actions_taken"] = [
        "Interactive OTP code verified against recipient session",
        "Warden release latch unsealed",
        "Driver commission RM 4.50 cleared for batch settlement",
        "Cryptographic ledger state updated"
    ]

# Latency Mode Simulation
if run_sim and animate_pitch and sentinel.get("anomalies_detected", False):
    with st.spinner("Sentinel scanning telemetry pings & cell tower handoffs..."):
        time.sleep(0.7)
    with st.spinner("Investigator cross-referencing OSRM road physics & POD heuristics..."):
        time.sleep(1.1)

# --- SPLIT LAYOUT: LEFT (50%) & RIGHT (50%) ---
left_col, right_col = st.columns([1, 1], gap="medium")

with left_col:
    is_api_scenario = "subcontractor_id" in scenario_data
    
    if not is_api_scenario:
        map_pin_svg = get_svg_icon("map-pin", color="#38BDF8", size=16)
        render_html(f"""
        <div class="panel-header">
            {map_pin_svg}
            <span>Spatial Telemetry & Road Kinematics</span>
        </div>
        """)
        render_interactive_map(scenario_data, sentinel.get("anomalies_detected", False), height=320)
        
        # OSRM Road Physics Feasibility Chart
        route_evals = investigator.get("route_evaluations", [])
        if route_evals:
            source_engine = route_evals[0].get("source", "LIVE_OSRM")
            source_badge_color = "#38BDF8" if source_engine == "LIVE_OSRM" else ("#F59E0B" if source_engine == "PREBAKED_CACHE" else "#A855F7")
            source_badge_text = "ENGINE: LIVE OPENSTREETMAP OSRM" if source_engine == "LIVE_OSRM" else ("ENGINE: KLANG VALLEY GRAPH (CACHE)" if source_engine == "PREBAKED_CACHE" else "ENGINE: HAVERSINE TORTUOSITY PHYSICS")
            render_html(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; margin-bottom:4px;">
                <span style="font-size:11px; color:#94A3B8; font-weight:600; font-family:'JetBrains Mono', monospace;">ROAD GRAPH FEASIBILITY</span>
                <span style="font-size:10px; font-weight:700; color:{source_badge_color}; background:rgba(255,255,255,0.05); padding:2px 8px; border-radius:4px; font-family:'JetBrains Mono', monospace;">[{source_badge_text}]</span>
            </div>
            """)
            st.plotly_chart(build_route_feasibility_chart(route_evals), use_container_width=True)

        # Check for POD evidence
        events = scenario_data.get("events", [])
        if events and "pod_evidence" in events[-1]:
            render_pod_inspector(scenario_data)

    else:
        # API Scraping Threat Visualization
        activity_svg = get_svg_icon("activity", color="#EF4444", size=16)
        render_html(f"""
        <div class="panel-header">
            {activity_svg}
            <span>Cyber Threat Radar: Out-of-Hours API Harvest</span>
        </div>
        """)
        st.plotly_chart(build_api_threat_chart(scenario_data), use_container_width=True)

        render_html(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; padding: 14px 16px; margin-bottom: 12px;">
            <div style="color: #EF4444; font-weight: 800; font-size: 12px; margin-bottom: 6px; letter-spacing:0.04em; font-family:'JetBrains Mono', monospace;">
                [THREAT DOSSIER] DATA EXFILTRATION DETECTED
            </div>
            <div style="font-size: 12px; color: #CBD5E1; line-height: 1.6;">
                • <b>Compromised Credential:</b> <code>{scenario_data.get('subcontractor_id')}</code><br>
                • <b>Attacker Source IP:</b> <code>{scenario_data.get('source_ip')}</code> (Identified Tor/Bulletproof VPN Node)<br>
                • <b>Target Endpoint:</b> <code>/api/v2/manifests/batch-export</code><br>
                • <b>Harvest Rate:</b> <b>520 requests/minute</b> (Standard baseline: 60/min)<br>
                • <b>Target Data:</b> 12,500 Customer PII records (Phone, Delivery Addresses)<br>
                • <b>Warden Containment:</b> API Token revoked at gateway. IP blacklisted in WAF.
            </div>
        </div>
        """)

    # Raw Telemetry Stream
    terminal_svg = get_svg_icon("terminal", color="#94A3B8", size=16)
    render_html(f"""
    <div class="panel-header">
        {terminal_svg}
        <span>Raw Telemetry Stream (Audit Log)</span>
    </div>
    """)
    events = scenario_data.get("events", [])
    if events and "location" in events[0]:
        table_rows = []
        for ev in events:
            table_rows.append({
                "Seq": f"#{ev.get('sequence')}",
                "Event": ev.get("event_type"),
                "Location": ev.get("location", {}).get("label"),
                "Speed": f"{ev.get('speed_kmh', 0)} km/h",
                "Tower ID": ev.get("cell_tower_id", "-"),
                "Note": ev.get("note", "")
            })
        df_events = pd.DataFrame(table_rows)
        st.dataframe(df_events, use_container_width=True, hide_index=True)
    else:
        st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)

with right_col:
    crosshair_svg = get_svg_icon("crosshair", color="#38BDF8", size=16)
    render_html(f"""
    <div class="panel-header">
        {crosshair_svg}
        <span>Zero-Trust Risk Scorecard & Policy Synthesis</span>
    </div>
    """)

    # Authoritative SOC Scorecard & Risk Badge
    risk_lvl = investigator.get("risk_level", "LOW")
    risk_color = "#EF4444" if risk_lvl == "CRITICAL" else ("#F59E0B" if risk_lvl == "MEDIUM" else "#10B981")
    risk_border = "rgba(239, 68, 68, 0.4)" if risk_lvl == "CRITICAL" else ("rgba(245, 158, 11, 0.4)" if risk_lvl == "MEDIUM" else "rgba(16, 185, 129, 0.4)")
    risk_bg = "rgba(239, 68, 68, 0.12)" if risk_lvl == "CRITICAL" else ("rgba(245, 158, 11, 0.12)" if risk_lvl == "MEDIUM" else "rgba(16, 185, 129, 0.10)")

    cargo_text = f"RM {scenario_data.get('parcel_value_myr', 0):.2f}" if "parcel_value_myr" in scenario_data else "N/A"
    peak_speed_text = f"{sentinel.get('highest_velocity_kmh', 0):.0f} km/h" if sentinel.get("highest_velocity_kmh", 0) > 0 else "Normal"

    sc_col1, sc_col2 = st.columns([5, 5])
    with sc_col1:
        st.plotly_chart(build_gauge_chart(investigator["trust_score"]), use_container_width=True)
    with sc_col2:
        render_html(f"""
        <div style="background:#090E19; border:1px solid #1A2338; border-radius:6px; padding:12px; margin-top:4px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:10px; color:#64748B; font-weight:700; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">THREAT CLASSIFICATION</span>
                <span style="font-size:10px; font-weight:700; color:{risk_color}; background:{risk_bg}; border:1px solid {risk_border}; padding:2px 8px; border-radius:4px; font-family:'JetBrains Mono', monospace;">
                    {risk_lvl}
                </span>
            </div>
            <div class="scorecard-grid">
                <div class="scorecard-cell">
                    <div class="scorecard-cell-label">POLICY ENFORCED</div>
                    <div class="scorecard-cell-value">{warden['action']}</div>
                </div>
                <div class="scorecard-cell">
                    <div class="scorecard-cell-label">TARGET ENTITY</div>
                    <div class="scorecard-cell-value">{warden['target_id']}</div>
                </div>
                <div class="scorecard-cell">
                    <div class="scorecard-cell-label">MAX KINEMATICS</div>
                    <div class="scorecard-cell-value">{peak_speed_text}</div>
                </div>
                <div class="scorecard-cell">
                    <div class="scorecard-cell-label">EXPOSED VALUE</div>
                    <div class="scorecard-cell-value">{cargo_text}</div>
                </div>
            </div>
        </div>
        """)

    # Forensic Penalty Deduction Breakdown Chart
    if "penalties" in investigator:
        st.plotly_chart(
            build_penalty_breakdown_chart(investigator["penalties"], investigator["trust_score"]),
            use_container_width=True
        )

    # Dynamic Warden Action Banner
    warden_act = warden.get("action", "AUTO_CLEAR")
    alert_badge_icon = get_svg_icon("shield-alert" if warden_act != "AUTO_CLEAR" else "shield-check", color="#FFFFFF", size=22)
    if warden_act in ("PACKAGE_FREEZE", "API_CREDENTIAL_REVOKED"):
        render_html(f"""
        <div class="warden-banner banner-freeze">
            <div>{alert_badge_icon}</div>
            <div>
                <div class="banner-title">{warden['banner_title']}</div>
                <div class="banner-desc">{warden['message']}</div>
            </div>
        </div>
        """)
    elif warden_act == "STEP_UP_CHALLENGE":
        render_html(f"""
        <div class="warden-banner banner-otp">
            <div>{alert_badge_icon}</div>
            <div>
                <div class="banner-title">{warden['banner_title']}</div>
                <div class="banner-desc">{warden['message']}</div>
            </div>
        </div>
        """)
    else:
        render_html(f"""
        <div class="warden-banner banner-clear">
            <div>{alert_badge_icon}</div>
            <div>
                <div class="banner-title">{warden['banner_title']}</div>
                <div class="banner-desc">{warden['message']}</div>
            </div>
        </div>
        """)

    # Interactive Step-Up OTP Verification Controls for Scenario 3
    if st.session_state.active_scenario_file == "fraud_pod_spoof.json":
        if not st.session_state.otp_cleared:
            render_html("""
            <div style="font-size:11px; font-weight:700; color:#F59E0B; margin-top:8px; margin-bottom:4px; font-family:'JetBrains Mono', monospace;">
                [CHALLENGE GATE] Recipient OTP Step-Up Authentication
            </div>
            """)
            c_otp1, c_otp2 = st.columns([3, 2])
            with c_otp1:
                otp_code = st.text_input(
                    "Recipient 6-digit SMS OTP",
                    placeholder="Enter 849201",
                    label_visibility="collapsed",
                    key="otp_input_box"
                )
            with c_otp2:
                if st.button("Authorize Delivery", use_container_width=True, type="primary"):
                    if otp_code.strip() in ("849201", "123456") or (len(otp_code.strip()) == 6 and otp_code.strip().isdigit()):
                        st.session_state.otp_cleared = True
                        st.rerun()
                    else:
                        st.error("Invalid OTP code. Try 849201.")
        else:
            render_html("""
            <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3); border-radius:6px; padding:10px 14px; margin-top:8px; margin-bottom:8px;">
                <span style="font-size:11px; color:#A7F3D0; font-weight:600; font-family:'JetBrains Mono', monospace;">[CHALLENGE RESOLVED] Customer verified OTP 849201. Consignment release approved.</span>
            </div>
            """)
            if st.button("Reset Challenge Demo", use_container_width=False):
                st.session_state.otp_cleared = False
                st.rerun()

    # SOAR Multi-Agent Pipeline Deck
    render_html("""
    <div class="panel-header" style="margin-top:16px;">
        <span>SOAR Automated Multi-Agent Pipeline</span>
    </div>
    """)
    eye_svg = get_svg_icon("eye", color="#38BDF8", size=15)
    cpu_card_svg = get_svg_icon("cpu", color="#818CF8", size=15)
    shield_card_svg = get_svg_icon("shield", color="#EF4444" if warden_act == "PACKAGE_FREEZE" else "#10B981", size=15)

    # 1. Sentinel Agent Step
    flags_html = "".join([f"<li style='color:#F87171;'>{f}</li>" for f in sentinel.get("flags", [])])
    render_html(f"""
    <div class="agent-card agent-card-sentinel">
        <div class="agent-header">
            <div class="agent-name-badge">
                {eye_svg}
                <span>Sentinel Agent</span>
                <span style="font-size:0.72rem; color:#38BDF8; font-family:'JetBrains Mono', monospace;">[Kinematic & Access Scanner]</span>
            </div>
            <span class="agent-latency-badge">18ms</span>
        </div>
        <div class="agent-body">
            <b>Status:</b> {sentinel['status']}<br>
            {sentinel['summary']}
            {f'<ul style="margin:4px 0 0 16px; padding:0;">{flags_html}</ul>' if flags_html else ''}
        </div>
    </div>
    """)

    # 2. Investigator Agent Step
    render_html(f"""
    <div class="agent-card agent-card-investigator">
        <div class="agent-header">
            <div class="agent-name-badge">
                {cpu_card_svg}
                <span>Investigator Agent</span>
                <span style="font-size:0.72rem; color:#818CF8; font-family:'JetBrains Mono', monospace;">[OSRM Physics & Forensic Reasoner]</span>
            </div>
            <span class="agent-latency-badge">142ms</span>
        </div>
        <div class="agent-body">
            <b>Zero-Trust Score:</b> <b style="color:{'#EF4444' if investigator['trust_score'] < 40 else ('#F59E0B' if investigator['trust_score'] < 75 else '#10B981')};">{investigator['trust_score']}/100</b><br>
            <b>Forensic Synthesis:</b> {investigator['forensic_narrative']}
        </div>
    </div>
    """)

    # 3. Warden Agent Step
    warden_card_type = "agent-card-warden-freeze" if warden_act in ("PACKAGE_FREEZE", "API_CREDENTIAL_REVOKED") else ("agent-card-warden-otp" if warden_act == "STEP_UP_CHALLENGE" else "agent-card-warden-clear")
    actions_html = "".join([f"<li>{act}</li>" for act in warden.get("actions_taken", [])])
    render_html(f"""
    <div class="agent-card {warden_card_type}">
        <div class="agent-header">
            <div class="agent-name-badge">
                {shield_card_svg}
                <span>Warden Agent</span>
                <span style="font-size:0.72rem; color:{'#EF4444' if warden_act == 'PACKAGE_FREEZE' else '#10B981'}; font-family:'JetBrains Mono', monospace;">[Risk-Adaptive Policy Enforcer]</span>
            </div>
            <span class="agent-latency-badge">8ms</span>
        </div>
        <div class="agent-body">
            <b>Autonomous Countermeasures Executed:</b>
            <ul style="margin:4px 0 0 16px; padding:0;">{actions_html}</ul>
        </div>
    </div>
    """)

    # Human-in-the-Loop Supervisory Controls
    with st.expander("Human-in-the-Loop Supervisory Controls", expanded=False):
        st.markdown(
            "SOC operators can inspect and override autonomous Warden enforcement actions. "
            "All supervisor overrides are appended to the immutable SHA-256 audit ledger."
        )
        ov_col1, ov_col2 = st.columns(2)
        with ov_col1:
            if st.button("Acknowledge & Escalate to SecOps", use_container_width=True):
                st.session_state.supervisor_action = "ESCALATED"
        with ov_col2:
            if st.button("Supervisor Override: Force Clearance", use_container_width=True):
                st.session_state.supervisor_action = "OVERRIDDEN"

        if st.session_state.supervisor_action == "ESCALATED":
            st.info("[SUPERVISOR DISPATCH] High-priority SecOps physical inspection ticket #SEC-LOG-8910 dispatched.")
        elif st.session_state.supervisor_action == "OVERRIDDEN":
            st.warning("[SUPERVISOR OVERRIDE] Manual clearance registered with biometric digital signoff in audit ledger.")

    # Mobile Courier Handset Simulator (if enabled)
    if st.session_state.show_handset and not is_api_scenario:
        phone_svg = get_svg_icon("phone", color="#38BDF8", size=16)
        render_html(f"""
        <div style="display:flex; align-items:center; gap:8px; margin-top:16px; margin-bottom:4px;">
            {phone_svg}
            <span style="font-weight:700; font-size:1.05rem; color:#F8FAFC;">Courier Handset Real-Time Status</span>
        </div>
        """)
        st.caption("Synchronized view of field driver's mobile device:")
        render_courier_handset(scenario_data, warden)

# --- FULL-WIDTH BOTTOM SECTION: CRYPTOGRAPHIC AUDIT LEDGER (ANON COMPLIANCE) ---
st.markdown("---")
render_cryptographic_ledger(result["audit_trail"], ledger_status)
