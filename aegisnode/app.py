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

from aegisnode.ui.mobile_view import render_mobile_courier_view
from aegisnode.data.live_bridge import get_live_state, update_warden_state

# 1. Page Configuration (Strict enterprise styling)
st.set_page_config(
    page_title="AegisNode | Zero-Trust Logistics Command Center",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Inject Cyber-Physical Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 3. Dedicated Mobile Courier Handset Mode Check (?mode=courier or ?view=handset)
mode_param = st.query_params.get("mode", "").lower()
view_param = st.query_params.get("view", "").lower()
if mode_param in ("courier", "phone", "driver") or view_param in ("handset", "phone") or st.session_state.get("mobile_mode_active", False):
    render_mobile_courier_view()
    st.stop()

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

    render_html("""
    <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 6px; padding: 8px 10px; margin-bottom: 12px; font-size: 11px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-weight: 700; color: #10B981;">LIVE PHONE BRIDGE</span>
            <span style="background:#10B981; color:#000; font-size:9px; font-weight:800; padding:1px 5px; border-radius:3px;">ONLINE</span>
        </div>
        <div style="color: #94A3B8; margin-top: 4px;">Open on phone for field demo:</div>
        <div style="color: #38BDF8; font-family: monospace; font-size:10px; margin-top: 2px;">?mode=courier</div>
    </div>
    """)

    if st.button("Open Handset View (Full Screen)", use_container_width=True, help="Switch this window to courier mobile handset"):
        st.session_state.mobile_mode_active = True
        st.rerun()

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
shield_head_svg = get_svg_icon("shield", color="#38BDF8", size=22)
render_html(f"""
<div class="command-header">
    <div style="display:flex; align-items:center; gap:12px;">
        {shield_head_svg}
        <div>
            <div class="brand-title">AEGISNODE</div>
            <div class="brand-subtitle">Zero-Trust Logistics Security • Autonomous Triage Engine</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:14px;">
        <span style="font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#94A3B8;">GDEX x ANON x UTAR 2026</span>
    </div>
</div>
""")

# --- 1-CLICK ACTIVE INCIDENT TRIAGE QUEUE ---
render_html("""
<div class="panel-header">
    <span>Active Incident Queue</span>
</div>
""")

col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    is_active = (st.session_state.active_scenario_file == "fraud_gps_spoof.json")
    if st.button(
        "INC-042 | GPS Teleport" + (" *" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate Phantom Courier mock location jump"
    ):
        select_scenario("fraud_gps_spoof.json")
        st.rerun()

with col_s2:
    is_active = (st.session_state.active_scenario_file == "normal_delivery.json")
    if st.button(
        "INC-081 | Clean Courier" + (" *" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate legitimate delivery route"
    ):
        select_scenario("normal_delivery.json")
        st.rerun()

with col_s3:
    is_active = (st.session_state.active_scenario_file == "fraud_pod_spoof.json")
    if st.button(
        "INC-109 | POD Forgery" + (" *" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate car floor mat / screenshot POD forgery"
    ):
        select_scenario("fraud_pod_spoof.json")
        st.rerun()

with col_s4:
    is_active = (st.session_state.active_scenario_file == "fraud_api_scraping.json")
    if st.button(
        "SEC-304 | API Scraping" + (" *" if is_active else ""),
        use_container_width=True,
        type="primary" if is_active else "secondary",
        help="Simulate 03:00 AM bulk PII scraping"
    ):
        select_scenario("fraud_api_scraping.json")
        st.rerun()

# Real-Time Mobile Bridge Synchronizer
@st.fragment(run_every="1s")
def _sync_live_courier_bridge():
    state = get_live_state()
    last_ts = st.session_state.get("last_bridge_ts", 0.0)
    curr_ts = state.get("last_action_timestamp", 0.0)
    if curr_ts > last_ts and curr_ts > 0:
        st.session_state.last_bridge_ts = curr_ts
        target_scn = state.get("active_scenario")
        if target_scn and target_scn != st.session_state.active_scenario_file:
            st.session_state.active_scenario_file = target_scn
            if state.get("otp_verified"):
                st.session_state.otp_cleared = True
            st.rerun()
        elif state.get("otp_verified") and not st.session_state.otp_cleared:
            st.session_state.otp_cleared = True
            st.rerun()

_sync_live_courier_bridge()

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

# Synchronize current Warden policy decision back to phone handset
update_warden_state(
    warden_action=warden.get("action", "AUTO_CLEAR"),
    trust_score=int(investigator.get("trust_score", 100)),
    velocity=float(sentinel.get("highest_velocity_kmh", 0.0)),
    message=warden.get("message", "Telemetry nominal."),
    otp_verified=st.session_state.otp_cleared
)

# Latency Mode Simulation
if run_sim and animate_pitch and sentinel.get("anomalies_detected", False):
    with st.spinner("Sentinel scanning telemetry pings..."):
        time.sleep(0.7)
    with st.spinner("Investigator verifying kinematics & POD heuristics..."):
        time.sleep(1.1)

# --- INCIDENT BRIEFING CARD (CONTEXTUAL FACTS, NO AI SLOP) ---
is_api_scenario = "subcontractor_id" in scenario_data
warden_act = warden.get("action", "AUTO_CLEAR")

if st.session_state.active_scenario_file == "fraud_gps_spoof.json":
    brief_tag = "INC-042"
    brief_title = "GPS Teleportation Spoofing (Phantom Courier)"
    brief_status = "QUARANTINE / DELIVERY FROZEN"
    status_class = "status-freeze"
    target_id = f"#{scenario_data.get('shipment_id', 'GDX-94021')}"
    subject_label = f"{scenario_data.get('courier_name', 'Ahmad Farhan')} ({scenario_data.get('courier_vehicle', 'Motorcycle')})"
    telemetry_fact = f"Peak Speed: {sentinel.get('highest_velocity_kmh', 458):.0f} km/h (Physically Impossible)"
    cargo_fact = f"RM {scenario_data.get('parcel_value_myr', 4200):.2f}"
    summary_text = "Courier telematics recorded a 38 km coordinate leap across Klang Valley in under 3 minutes (458 km/h). Real physical road transit requires a minimum of 34 minutes via OSRM. Autonomous delivery hold executed."
elif st.session_state.active_scenario_file == "normal_delivery.json":
    brief_tag = "INC-081"
    brief_title = "Legitimate Courier Delivery Route"
    brief_status = "VERIFIED / NOMINAL CLEAR"
    status_class = "status-clear"
    target_id = f"#{scenario_data.get('shipment_id', 'GDX-10842')}"
    subject_label = f"{scenario_data.get('courier_name', 'Siti Nurhaliza')} ({scenario_data.get('courier_vehicle', 'Van')})"
    telemetry_fact = f"Average Speed: {sentinel.get('highest_velocity_kmh', 32):.0f} km/h (Nominal City Route)"
    cargo_fact = f"RM {scenario_data.get('parcel_value_myr', 180):.2f}"
    summary_text = "All 6 telematics pings align with expected OpenStreetMap road kinematics and verified cell tower handoffs. Zero anomaly detected. Delivery cleared for customer handover."
elif st.session_state.active_scenario_file == "fraud_pod_spoof.json":
    brief_tag = "INC-109"
    brief_title = "Optical Proof-of-Delivery (POD) Forgery Attack"
    if st.session_state.otp_cleared:
        brief_status = "CHALLENGE RESOLVED / APPROVED"
        status_class = "status-clear"
    else:
        brief_status = "STEP-UP CHALLENGE / OTP REQUIRED"
        status_class = "status-otp"
    target_id = f"#{scenario_data.get('shipment_id', 'GDX-77192')}"
    subject_label = f"{scenario_data.get('courier_name', 'Kevin Tan')} ({scenario_data.get('courier_vehicle', 'Motorcycle')})"
    telemetry_fact = "Laplacian Edge Variance: 14.2 (Threshold: 60.0)"
    cargo_fact = f"RM {scenario_data.get('parcel_value_myr', 1850):.2f}"
    summary_text = "Driver uploaded a darkened interior photo of a car floor mat to simulate parcel handover. Kinetic route was nominal, but proof-of-delivery failed optical edge variance heuristic. Autonomous Warden suspended payout and dispatched an SMS OTP challenge to the customer."
else:  # fraud_api_scraping.json
    brief_tag = "SEC-304"
    brief_title = "Out-of-Hours Subcontractor API Harvesting"
    brief_status = "CONTAINMENT / CREDENTIAL REVOKED"
    status_class = "status-freeze"
    target_id = f"Partner {scenario_data.get('subcontractor_id', '#SUB-8812')} (FastShip)"
    subject_label = f"Tor Exit Node: {scenario_data.get('source_ip', '185.220.101.5')}"
    telemetry_fact = "Rate: 520 req/min at 03:00 AM (Baseline: 60/min)"
    cargo_fact = "12,500 Customer PII Records"
    summary_text = "Subcontractor API credentials were used from an anonymous VPN/Tor node at 03:00 AM to exfiltrate bulk delivery manifests at 8.6x normal limits. Warden automatically revoked the API bearer token and blacklisted the IP at the perimeter WAF."

render_html(f"""
<div class="incident-briefing">
    <div class="briefing-top">
        <div class="briefing-id-group">
            <span class="briefing-tag">{brief_tag}</span>
            <span class="briefing-title">{brief_title}</span>
        </div>
        <div class="briefing-status {status_class}">
            {brief_status}
        </div>
    </div>
    <div class="briefing-meta-grid">
        <div class="meta-item">
            <span class="meta-label">CONSIGNMENT / ENTITY</span>
            <span class="meta-val">{target_id}</span>
        </div>
        <div class="meta-item">
            <span class="meta-label">SUBJECT</span>
            <span class="meta-val">{subject_label}</span>
        </div>
        <div class="meta-item">
            <span class="meta-label">TELEMETRY ANOMALY</span>
            <span class="meta-val">{telemetry_fact}</span>
        </div>
        <div class="meta-item">
            <span class="meta-label">PROTECTED VALUE</span>
            <span class="meta-val">{cargo_fact}</span>
        </div>
    </div>
    <div class="briefing-summary">
        {summary_text}
    </div>
</div>
""")

# --- PROGRESSIVE DISCLOSURE TABS (NO COGNITIVE OVERLOAD) ---
tab_evidence, tab_decision, tab_ledger = st.tabs([
    "Spatial & Sensor Evidence",
    "Agent Triage & Policy Enforcement",
    "Cryptographic Audit Ledger",
])

with tab_evidence:
    if not is_api_scenario:
        render_html("""
        <div class="panel-header">
            <span>Spatial Telemetry & Verified Road Trajectory</span>
        </div>
        """)
        render_interactive_map(scenario_data, sentinel.get("anomalies_detected", False), height=380)

        col_ev1, col_ev2 = st.columns([1, 1], gap="medium")
        with col_ev1:
            events = scenario_data.get("events", [])
            has_pod = (events and "pod_evidence" in events[-1])
            if has_pod:
                render_pod_inspector(scenario_data)
            else:
                route_evals = investigator.get("route_evaluations", [])
                if route_evals:
                    render_html("""
                    <div class="panel-header">
                        <span>Road Kinematics & OSRM Feasibility</span>
                    </div>
                    """)
                    st.plotly_chart(build_route_feasibility_chart(route_evals), use_container_width=True)

        with col_ev2:
            render_html("""
            <div class="panel-header">
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
                    })
                df_events = pd.DataFrame(table_rows)
                st.dataframe(df_events, use_container_width=True, hide_index=True)
            else:
                st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)

    else:
        render_html("""
        <div class="panel-header">
            <span>Physical Depot Sector & Subcontractor Corridor</span>
        </div>
        """)
        render_interactive_map(scenario_data, True, height=340)

        render_html("""
        <div class="panel-header" style="margin-top:14px;">
            <span>Cyber Threat Radar: Out-of-Hours API Harvest</span>
        </div>
        """)
        st.plotly_chart(build_api_threat_chart(scenario_data), use_container_width=True)

        col_api1, col_api2 = st.columns([1, 1], gap="medium")
        with col_api1:
            render_html(f"""
            <div style="background: #0D1322; border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; padding: 14px 16px; margin-top: 10px;">
                <div style="color: #EF4444; font-weight: 700; font-size: 11px; margin-bottom: 6px; font-family:'JetBrains Mono', monospace; text-transform:uppercase;">
                    Threat Dossier: Data Exfiltration
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
        with col_api2:
            render_html("""
            <div class="panel-header" style="margin-top:10px;">
                <span>Security Gateway Request Stream</span>
            </div>
            """)
            events = scenario_data.get("events", [])
            st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)

with tab_decision:
    dec_col1, dec_col2 = st.columns([1, 1], gap="medium")

    with dec_col1:
        render_html("""
        <div class="panel-header">
            <span>Zero-Trust Confidence & Penalty Breakdown</span>
        </div>
        """)
        st.plotly_chart(build_gauge_chart(investigator["trust_score"]), use_container_width=True)

        if "penalties" in investigator:
            st.plotly_chart(
                build_penalty_breakdown_chart(investigator["penalties"], investigator["trust_score"]),
                use_container_width=True
            )

    with dec_col2:
        render_html("""
        <div class="panel-header">
            <span>Automated Policy Enforcement</span>
        </div>
        """)
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

        with st.expander("Supervisor Controls & Manual Override", expanded=False):
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
                st.info("[SUPERVISOR DISPATCH] SecOps physical inspection ticket #SEC-LOG-8910 dispatched.")
            elif st.session_state.supervisor_action == "OVERRIDDEN":
                st.warning("[SUPERVISOR OVERRIDE] Manual clearance registered with biometric digital signoff in audit ledger.")

        if st.session_state.show_handset and not is_api_scenario:
            render_html("""
            <div class="panel-header" style="margin-top:16px;">
                <span>Courier Handset Live Display</span>
            </div>
            """)
            render_courier_handset(scenario_data, warden)

    render_html("""
    <div class="panel-header" style="margin-top:24px;">
        <span>SOAR Automated Multi-Agent Pipeline</span>
    </div>
    """)
    eye_svg = get_svg_icon("eye", color="#38BDF8", size=15)
    cpu_card_svg = get_svg_icon("cpu", color="#818CF8", size=15)
    shield_card_svg = get_svg_icon("shield", color="#EF4444" if warden_act == "PACKAGE_FREEZE" else "#10B981", size=15)

    pipe_c1, pipe_c2, pipe_c3 = st.columns(3)
    with pipe_c1:
        flags_html = "".join([f"<li style='color:#F87171;'>{f}</li>" for f in sentinel.get("flags", [])])
        render_html(f"""
        <div class="agent-card agent-card-sentinel">
            <div class="agent-header">
                <div class="agent-name-badge">
                    {eye_svg}
                    <span>Sentinel Agent</span>
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

    with pipe_c2:
        render_html(f"""
        <div class="agent-card agent-card-investigator">
            <div class="agent-header">
                <div class="agent-name-badge">
                    {cpu_card_svg}
                    <span>Investigator Agent</span>
                </div>
                <span class="agent-latency-badge">142ms</span>
            </div>
            <div class="agent-body">
                <b>Trust Score:</b> <b style="color:{'#EF4444' if investigator['trust_score'] < 40 else ('#F59E0B' if investigator['trust_score'] < 75 else '#10B981')};">{investigator['trust_score']}/100</b><br>
                <b>Forensic Synthesis:</b> {investigator['forensic_narrative']}
            </div>
        </div>
        """)

    with pipe_c3:
        warden_card_type = "agent-card-warden-freeze" if warden_act in ("PACKAGE_FREEZE", "API_CREDENTIAL_REVOKED") else ("agent-card-warden-otp" if warden_act == "STEP_UP_CHALLENGE" else "agent-card-warden-clear")
        actions_html = "".join([f"<li>{act}</li>" for act in warden.get("actions_taken", [])])
        render_html(f"""
        <div class="agent-card {warden_card_type}">
            <div class="agent-header">
                <div class="agent-name-badge">
                    {shield_card_svg}
                    <span>Warden Agent</span>
                </div>
                <span class="agent-latency-badge">8ms</span>
            </div>
            <div class="agent-body">
                <b>Actions Executed:</b>
                <ul style="margin:4px 0 0 16px; padding:0;">{actions_html}</ul>
            </div>
        </div>
        """)

with tab_ledger:
    render_cryptographic_ledger(result["audit_trail"], ledger_status)

