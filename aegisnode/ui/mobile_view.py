"""
AegisNode - Mobile Courier Handset Interface
Dedicated full-screen mobile smartphone view for physical field demonstrations.
Zero Emojis - Enterprise Cyber-Physical Security.
"""

import streamlit as st
from aegisnode.data.live_bridge import get_live_state, update_courier_action
from aegisnode.ui.styles import get_svg_icon, render_html

def render_mobile_courier_view():
    """
    Renders an edge courier handset interface optimized for smartphones.
    Allows a courier holding a real phone to trigger fraud vectors and receive Warden lockdowns.
    """
    # Custom high-contrast mobile CSS
    st.markdown("""
    <style>
        .mobile-shell {
            max-width: 440px;
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
        .mobile-btn {
            display: block;
            width: 100%;
            padding: 12px 16px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
            text-align: center;
            margin-bottom: 10px;
            cursor: pointer;
            border: none;
        }
        .status-box-freeze {
            background: rgba(239, 68, 68, 0.12);
            border: 2px solid #EF4444;
            color: #FCA5A5;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 16px;
        }
        .status-box-challenge {
            background: rgba(245, 158, 11, 0.12);
            border: 2px solid #F59E0B;
            color: #FCD34D;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 16px;
        }
        .status-box-clear {
            background: rgba(16, 185, 129, 0.12);
            border: 2px solid #10B981;
            color: #6EE7B7;
            padding: 14px;
            border-radius: 10px;
            margin-bottom: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

    _render_mobile_body()

@st.fragment(run_every="1s")
def _render_mobile_body():
    state = get_live_state()
    warden_act = state.get("warden_action", "AUTO_CLEAR")
    velocity = state.get("highest_velocity_kmh", 0.0)
    score = state.get("trust_score", 100)
    otp_verified = state.get("otp_verified", False)

    phone_svg = get_svg_icon("phone", color="#38BDF8", size=18)
    shield_svg = get_svg_icon("shield", color="#10B981", size=16)

    st.markdown(f"""
    <div class="mobile-shell">
        <div class="mobile-header">
            <div style="display:flex; align-items:center; gap:8px;">
                {phone_svg}
                <span style="font-weight:800; font-size:14px; color:#F8FAFC;">GDEX Courier Go v4.2</span>
            </div>
            <span class="mobile-badge badge-live">LIVE BRIDGE ACTIVE</span>
        </div>
        <div class="mobile-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:11px; color:#94A3B8;">CONSIGNMENT:</span>
                <span style="font-size:12px; font-weight:700; color:#38BDF8; font-family:'JetBrains Mono', monospace;">#GDX-SHP-20261003-042</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:11px; color:#94A3B8;">CARGO:</span>
                <span style="font-size:11px; font-weight:600; color:#F1F5F9;">iPhone 17 Pro (RM 1,850.00)</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:11px; color:#94A3B8;">RECIPIENT:</span>
                <span style="font-size:11px; font-weight:600; color:#F1F5F9;">Sarah Lim (Menara PJX, PJ)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. Real-time Security Latch Status
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
                Proof-of-delivery photo flagged as synthetic/recycled.
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

    # 2. Interactive Field Attack Triggers
    st.markdown("<div style='font-size:11px; font-weight:700; color:#64748B; margin: 12px 0 8px 0; text-transform:uppercase;'>Simulate Field Operations:</div>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Simulate Mock GPS Spoof", type="secondary", use_container_width=True, help="Teleport 15 km in 2 mins"):
            update_courier_action("TRIGGER_GPS_SPOOF", "fraud_gps_spoof.json")
            st.rerun()

    with col_btn2:
        if st.button("Upload Fake POD Photo", type="secondary", use_container_width=True, help="Submit car floor mat photo"):
            update_courier_action("TRIGGER_POD_FORGERY", "fraud_pod_spoof.json")
            st.rerun()

    col_btn3, col_btn4 = st.columns(2)
    with col_btn3:
        if st.button("Complete Clean Delivery", type="primary", use_container_width=True, help="Legitimate dropoff"):
            update_courier_action("TRIGGER_NORMAL_DELIVERY", "normal_delivery.json")
            st.rerun()

    with col_btn4:
        if st.button("Reset Session", use_container_width=True, help="Reset handset and SOC bridge"):
            update_courier_action("STANDBY", "normal_delivery.json")
            st.rerun()

    st.markdown("""
        <div style="text-align:center; margin-top:14px; font-size:10px; color:#64748B; font-family:'JetBrains Mono', monospace;">
            AegisNode Edge Daemon Polling: 1.0s | GDEX Secure Net
        </div>
    </div>
    """, unsafe_allow_html=True)
