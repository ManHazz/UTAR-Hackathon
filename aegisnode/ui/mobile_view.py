"""
AegisNode - Mobile Courier Handset Interface
Dedicated full-screen mobile smartphone view for physical field demonstrations.
Acquires real hardware GPS from phone and captures live photos via device camera.
Strict enterprise compliance - Zero Emojis.
"""

from typing import Optional
from pathlib import Path
import streamlit as st

from aegisnode.data.live_bridge import (
    get_live_state,
    update_courier_action,
    update_courier_telematics,
    add_route_waypoint,
    clear_route_history,
    trigger_gps_spoof,
    process_uploaded_pod_photo,
    reset_live_state,
)
from aegisnode.ui.styles import get_svg_icon, render_html

def render_mobile_courier_view():
    """
    Renders an edge courier handset interface optimized for smartphones.
    Zero race conditions: eliminates timed auto-refresh fragments that cause white screen crashes.
    """
    st.markdown("""
    <style>
        .mobile-shell {
            max-width: 480px;
            margin: 0 auto;
            background: #0B0F17;
            border: 1px solid #1E293B;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .mobile-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1E293B;
            padding-bottom: 10px;
            margin-bottom: 14px;
        }
        .mobile-badge {
            font-size: 10px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .badge-live {
            background: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .mobile-card {
            background: #111827;
            border: 1px solid #1F2937;
            border-radius: 10px;
            padding: 12px 14px;
            margin-bottom: 12px;
        }
        .status-box-freeze {
            background: rgba(239, 68, 68, 0.12);
            border: 2px solid #EF4444;
            color: #FCA5A5;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 14px;
        }
        .status-box-challenge {
            background: rgba(245, 158, 11, 0.12);
            border: 2px solid #F59E0B;
            color: #FCD34D;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 14px;
        }
        .status-box-clear {
            background: rgba(16, 185, 129, 0.12);
            border: 2px solid #10B981;
            color: #6EE7B7;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 14px;
        }
        .coord-pill {
            display: inline-block;
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.25);
            color: #38BDF8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            padding: 3px 7px;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    state = get_live_state()

    # Top Switcher: Allows smooth exit back to Desktop SOC Command Center
    col_top1, col_top2 = st.columns([2, 1])
    with col_top1:
        st.caption("Courier Handset Operating Surface")
    with col_top2:
        if st.button("Switch to SOC View", use_container_width=True, help="Switch view back to desktop SOC command center"):
            st.session_state.mobile_mode_active = False
            if "mode" in st.query_params:
                del st.query_params["mode"]
            if "view" in st.query_params:
                del st.query_params["view"]
            st.rerun()

    # 1. Check for URL Query Coordinates passed from browser GPS
    query_lat = st.query_params.get("lat")
    query_lon = st.query_params.get("lon")
    if query_lat and query_lon:
        try:
            parsed_lat = float(query_lat)
            parsed_lon = float(query_lon)
            if abs(parsed_lat - state.get("courier_lat", 0.0)) > 0.0001 or abs(parsed_lon - state.get("courier_lon", 0.0)) > 0.0001:
                update_courier_telematics(parsed_lat, parsed_lon, label="Phone GPS Hardware Fix")
                state = get_live_state()
        except Exception:
            pass

    cur_lat = state.get("courier_lat", 4.385200)
    cur_lon = state.get("courier_lon", 100.978100)
    cur_label = state.get("courier_location_label", "UTP Campus, Tronoh, Perak")
    warden_act = state.get("warden_action", "AUTO_CLEAR")
    velocity = state.get("highest_velocity_kmh", 0.0)
    score = state.get("trust_score", 100)
    otp_verified = state.get("otp_verified", False)

    phone_svg = get_svg_icon("phone", color="#38BDF8", size=18)

    st.markdown(f"""
    <div class="mobile-shell">
        <div class="mobile-header">
            <div style="display:flex; align-items:center; gap:8px;">
                {phone_svg}
                <span style="font-weight:800; font-size:14px; color:#F8FAFC;">GDEX Courier Go v4.2</span>
            </div>
            <span class="mobile-badge badge-live">SOC BRIDGE ACTIVE</span>
        </div>
        <div class="mobile-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:11px; color:#94A3B8;">CONSIGNMENT:</span>
                <span style="font-size:12px; font-weight:700; color:#38BDF8; font-family:'JetBrains Mono', monospace;">#GDX-SHP-20261003-042</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:11px; color:#94A3B8;">DRIVER:</span>
                <span style="font-size:11px; font-weight:600; color:#F1F5F9;">Ahmad Farhan (Motorcycle)</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:11px; color:#94A3B8;">CARGO:</span>
                <span style="font-size:11px; font-weight:600; color:#F1F5F9;">iPhone 17 Pro (RM 1,850.00)</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:11px; color:#94A3B8;">DESTINATION:</span>
                <span style="font-size:11px; font-weight:600; color:#F1F5F9;">Chancellor Hall, UTP</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. HARDWARE TELEMATICS & GPS POSITION SENSOR
    st.markdown("<div style='font-size:11px; font-weight:700; color:#38BDF8; margin: 12px 0 6px 0; text-transform:uppercase;'>1. Phone Hardware GPS Telematics:</div>", unsafe_allow_html=True)

    route_history = state.get("route_history", [])
    history_count = len(route_history)

    st.markdown(f"""
    <div style="background:#111827; border:1px solid #1F2937; border-radius:10px; padding:12px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:11px; color:#94A3B8;">CURRENT POSITION:</span>
            <span class="coord-pill">{cur_lat:.5f} N, {cur_lon:.5f} E</span>
        </div>
        <div style="font-size:12px; font-weight:600; color:#F8FAFC; margin-bottom:6px;">
            {cur_label}
        </div>
        <div style="display:flex; justify-content:space-between; font-size:10px; color:#38BDF8; font-family:monospace;">
            <span>Recorded Route: <b>{history_count} checkpoints</b></span>
            <span style="color:#10B981;">Tower #TWR-UTP-01</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Campus Waypoints for tracing real route around UTP
    st.markdown("<div style='font-size:10px; font-weight:700; color:#94A3B8; margin-bottom:4px; text-transform:uppercase;'>UTP Campus Waypoints (1-Tap Trace):</div>", unsafe_allow_html=True)
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        if st.button("[+] UTP Main Gate", use_container_width=True, help="Add UTP Main Gate to route"):
            add_route_waypoint(4.388500, 100.967500, "UTP Main Gate Checkpoint (Tronoh)", speed_kmh=28.0)
            st.rerun()
        if st.button("[+] Chancellor Hall", use_container_width=True, help="Add Chancellor Hall to route"):
            add_route_waypoint(4.383500, 100.972000, "UTP Chancellor Hall Delivery Zone", speed_kmh=25.0)
            st.rerun()
        if st.button("[+] Pocket D (CS)", use_container_width=True, help="Add Pocket D to route"):
            add_route_waypoint(4.381800, 100.974500, "UTP Pocket D / Computer Science", speed_kmh=30.0)
            st.rerun()
    with col_w2:
        if st.button("[+] Oval Park", use_container_width=True, help="Add Oval Park to route"):
            add_route_waypoint(4.386200, 100.971200, "UTP Oval Park / Info Center", speed_kmh=32.0)
            st.rerun()
        if st.button("[+] IRC Main Library", use_container_width=True, help="Add IRC Library to route"):
            add_route_waypoint(4.384600, 100.970200, "UTP IRC Main Library", speed_kmh=25.0)
            st.rerun()
        if st.button("[+] Village 4", use_container_width=True, help="Add Village 4 to route"):
            add_route_waypoint(4.387200, 100.976800, "UTP Village 4 Residential", speed_kmh=28.0)
            st.rerun()

    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("[+] Log Current Fix", use_container_width=True, help="Log current GPS position as route checkpoint"):
            add_route_waypoint(cur_lat, cur_lon, f"Fix #{history_count+1}: {cur_label}", speed_kmh=30.0)
            st.rerun()
    with col_act2:
        if st.button("Reset Route Path", use_container_width=True, help="Clear breadcrumbs and start route fresh"):
            clear_route_history(cur_lat, cur_lon, cur_label)
            st.rerun()

    # Browser Geolocation JS Widget (Safe, no parent window redirection)
    st.components.v1.html("""
    <div style="font-family:-apple-system,BlinkMacSystemFont,sans-serif; text-align:center; padding:6px 0;">
        <button id="gps-btn" onclick="acquireGPS()" style="width:100%; background:#0284C7; color:#FFFFFF; border:none; border-radius:8px; padding:10px 14px; font-size:12px; font-weight:700; cursor:pointer;">
            [GPS] Acquire Live Phone GPS Fix
        </button>
        <div id="gps-status" style="margin-top:6px; font-size:11px; color:#94A3B8;">
            Tap to query device GPS sensor via browser API
        </div>
        <div id="gps-confirm-box" style="margin-top:8px; display:none;"></div>
    </div>
    <script>
    function acquireGPS() {
        var btn = document.getElementById("gps-btn");
        var st = document.getElementById("gps-status");
        var box = document.getElementById("gps-confirm-box");
        if (!navigator.geolocation) {
            st.innerHTML = "<span style='color:#EF4444'>Geolocation not supported by this browser</span>";
            return;
        }
        btn.innerText = "Querying GPS Satellites...";
        navigator.geolocation.getCurrentPosition(
            function(pos) {
                var lat = pos.coords.latitude.toFixed(6);
                var lon = pos.coords.longitude.toFixed(6);
                var acc = pos.coords.accuracy.toFixed(1);
                st.innerHTML = "<span style='color:#10B981; font-weight:700;'>GPS Locked: " + lat + ", " + lon + " (±" + acc + "m)</span>";
                btn.innerText = "GPS Fix Acquired";
                box.style.display = "block";
                box.innerHTML = "<a href='?mode=courier&lat=" + lat + "&lon=" + lon + "' target='_top' style='display:block; width:100%; background:#10B981; color:#0B0F17; font-weight:800; font-size:12px; padding:10px 12px; border-radius:6px; text-decoration:none;'>[TAP TO LOCK YOUR LIVE GPS: " + lat + ", " + lon + "]</a>";
            },
            function(err) {
                btn.innerText = "Retry GPS Query";
                st.innerHTML = "<span style='color:#F59E0B'>GPS prompt: " + err.message + "</span>";
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
        );
    }
    </script>
    """, height=125)

    with st.expander("Fine-Tune Exact GPS Coordinates", expanded=False):
        c_lat, c_lon = st.columns(2)
        with c_lat:
            in_lat = st.number_input("Latitude", value=cur_lat, format="%.6f")
        with c_lon:
            in_lon = st.number_input("Longitude", value=cur_lon, format="%.6f")
        if st.button("Apply Coordinates", use_container_width=True):
            update_courier_telematics(in_lat, in_lon, label="Custom Hardware Fix")
            st.rerun()

    # 3. LIVE PROOF-OF-DELIVERY (POD) PHOTO CAPTURE
    st.markdown("<div style='font-size:11px; font-weight:700; color:#38BDF8; margin: 10px 0 6px 0; text-transform:uppercase;'>2. Live Optical POD Verification:</div>", unsafe_allow_html=True)
    st.caption("Snap physical parcel with phone camera. OpenCV Laplacian evaluates edge texture in real time.")

    camera_pic = st.camera_input("Snap Live POD Photo with Phone Camera", label_visibility="collapsed")
    if camera_pic is not None:
        pic_bytes = camera_pic.getvalue()
        process_uploaded_pod_photo(pic_bytes)
        st.success("POD photo processed and transmitted to SOC Command Center.")

    # Alternative file uploader for testing photos
    with st.expander("Or select image file from gallery", expanded=False):
        uploaded_file = st.file_uploader("Upload POD Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if uploaded_file is not None:
            pic_bytes = uploaded_file.getvalue()
            process_uploaded_pod_photo(pic_bytes)
            st.success("Uploaded photo transmitted to SOC.")

    # If photo exists, show forensic summary
    if state.get("has_live_photo"):
        photo_status = state.get("live_photo_status", "VALID")
        var_score = state.get("live_photo_variance", 0.0)
        badge_col = "#EF4444" if photo_status == "FORGED" else "#10B981"
        st.markdown(f"""
        <div style="background:#111827; border:1px solid #1F2937; border-radius:8px; padding:8px 12px; margin-bottom:12px; font-size:11px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#94A3B8;">OPTICAL FORENSIC STATUS:</span>
                <span style="color:{badge_col}; font-weight:800;">[{photo_status}]</span>
            </div>
            <div style="color:#F1F5F9; margin-top:3px;">
                Laplacian Edge Variance: <b>{var_score:.1f}</b> (Threshold: 55.0)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. REAL-TIME WARDEN POLICY LATCH STATUS
    st.markdown("<div style='font-size:11px; font-weight:700; color:#38BDF8; margin: 10px 0 6px 0; text-transform:uppercase;'>3. Terminal Security Latch:</div>", unsafe_allow_html=True)

    if warden_act == "PACKAGE_FREEZE":
        st.markdown(f"""
        <div class="status-box-freeze">
            <div style="font-weight:800; font-size:13px; text-transform:uppercase; margin-bottom:4px; letter-spacing:0.04em; color:#EF4444;">
                [ALERT] TERMINAL LOCKED BY WARDEN
            </div>
            <div style="font-size:12px; line-height:1.5;">
                Kinematic speed violation detected (<b>{velocity:.0f} km/h</b>).
                <br><b>Trust Score: {score}/100</b>
                <br>Payout frozen. Consignment quarantined. Report to Shah Alam Section 23 hub.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif warden_act == "STEP_UP_CHALLENGE" and not otp_verified:
        st.markdown(f"""
        <div class="status-box-challenge">
            <div style="font-weight:800; font-size:13px; text-transform:uppercase; margin-bottom:4px; letter-spacing:0.04em; color:#F59E0B;">
                [SECURITY CHALLENGE] CUSTOMER OTP REQUIRED
            </div>
            <div style="font-size:12px; line-height:1.5;">
                Proof-of-delivery photo flagged as low-texture / floor mat.
                <br><b>Trust Score: {score}/100</b>
                <br>Obtain the 6-digit verification code sent to customer Sarah Lim.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_inp, col_sub = st.columns([2, 1])
        with col_inp:
            otp_val = st.text_input("6-Digit Code", placeholder="849201", label_visibility="collapsed")
        with col_sub:
            if st.button("Verify OTP", type="primary", use_container_width=True):
                update_courier_action("SUBMIT_OTP", "fraud_pod_spoof.json", otp_code=otp_val)
                st.rerun()

    else:
        st.markdown(f"""
        <div class="status-box-clear">
            <div style="font-weight:800; font-size:13px; text-transform:uppercase; margin-bottom:4px; letter-spacing:0.04em; color:#10B981;">
                [STATUS: VERIFIED] NOMINAL TRANSIT
            </div>
            <div style="font-size:12px; line-height:1.5;">
                Zero-trust telemetry, kinematics, and proof validated.
                <br><b>Trust Score: {score}/100</b> | Payout approved: <b>+RM 4.50</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. INTERACTIVE TELEMATICS & KINEMATICS TEST SANDBOX
    st.markdown("<div style='font-size:11px; font-weight:700; color:#64748B; margin: 12px 0 8px 0; text-transform:uppercase;'>Interactive Telematics & Kinematics Testing:</div>", unsafe_allow_html=True)

    with st.expander("Telematics Spoof & Speed Injector", expanded=False):
        st.caption("Test how the AI Agent evaluates physical kinematics by injecting coordinate jumps across different travel times.")
        
        target_choice = st.selectbox(
            "Target Destination",
            options=[
                "Menara PJX, Petaling Jaya (185.3 km)",
                "KLCC Twin Towers, Kuala Lumpur (198.5 km)",
                "Ipoh Station 18 Hub, Perak (32.4 km)",
            ]
        )
        duration_choice = st.selectbox(
            "Elapsed Travel Duration",
            options=[
                "2.0 minutes (Mock Location Injection -> ~5,500 km/h)",
                "15.0 minutes (High-Speed Transit -> ~740 km/h)",
                "120.0 minutes (Feasible Highway Route -> ~92 km/h)",
            ]
        )

        dest_coords = {
            "Menara PJX, Petaling Jaya (185.3 km)": (3.103200, 101.644500, "Menara PJX, Petaling Jaya"),
            "KLCC Twin Towers, Kuala Lumpur (198.5 km)": (3.157800, 101.711800, "KLCC, Kuala Lumpur"),
            "Ipoh Station 18 Hub, Perak (32.4 km)": (4.551200, 101.071800, "Ipoh Station 18, Perak"),
        }
        dur_mins = {
            "2.0 minutes (Mock Location Injection -> ~5,500 km/h)": 2.0,
            "15.0 minutes (High-Speed Transit -> ~740 km/h)": 15.0,
            "120.0 minutes (Feasible Highway Route -> ~92 km/h)": 120.0,
        }

        if st.button("Inject Coordinate Jump Test", use_container_width=True, type="secondary"):
            t_lat, t_lon, t_lbl = dest_coords[target_choice]
            d_min = dur_mins[duration_choice]
            trigger_gps_spoof(
                start_lat=cur_lat,
                start_lon=cur_lon,
                target_lat=t_lat,
                target_lon=t_lon,
                start_label=cur_label,
                target_label=t_lbl,
                elapsed_minutes=d_min
            )
            st.rerun()

    col_btn3, col_btn4 = st.columns(2)
    with col_btn3:
        if st.button("Submit Clean Delivery", type="primary", use_container_width=True, help="Legitimate handover"):
            update_courier_action("TRIGGER_NORMAL_DELIVERY", "normal_delivery.json")
            st.rerun()

    with col_btn4:
        if st.button("Reset Terminal", use_container_width=True, help="Reset to nominal state"):
            reset_live_state()
            st.rerun()

    st.markdown("""
        <div style="text-align:center; margin-top:14px; font-size:10px; color:#64748B; font-family:'JetBrains Mono', monospace;">
            AegisNode Edge Daemon | Direct Cyber-Physical Bridge
        </div>
    """, unsafe_allow_html=True)
