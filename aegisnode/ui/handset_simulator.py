"""
AegisNode - Mobile Courier Handset Simulator
Shows real-time operational impact on the driver's smartphone handset screen.
Enterprise operational preview - Zero Emojis.
"""

from typing import Dict, Any
import streamlit as st
from aegisnode.ui.styles import get_svg_icon, render_html

def render_courier_handset(scenario_data: Dict[str, Any], warden_result: Dict[str, Any]):
    """
    Renders an interactive smartphone mockup showing the courier's real-time app screen
    without raw markdown indentation bugs.
    """
    action = warden_result.get("action", "AUTO_CLEAR")
    shipment_id = scenario_data.get("shipment_id", "GDX-PACKAGE")
    courier_name = scenario_data.get("courier_name", "Courier")
    cargo_value = scenario_data.get("parcel_value_myr", 0.0)
    recipient = scenario_data.get("recipient_name", "Recipient")

    wifi_icon = get_svg_icon("wifi", color="#94A3B8", size=12)
    battery_icon = get_svg_icon("battery", color="#94A3B8", size=14)

    if action == "AUTO_CLEAR":
        theme_color = "#10B981"
        header_badge = "STATUS: VERIFIED"
        title = "Delivery Verified and Recorded"
        body = f"Consignment <b>{shipment_id}</b> successfully handed to <b>{recipient}</b>.<br><br>Zero-trust telemetry, kinematics, and proof-of-delivery validated."
        btn_text = "Payout Approved: +RM 4.50"
        btn_class = "btn-handset-success"
    elif action == "STEP_UP_CHALLENGE":
        theme_color = "#F59E0B"
        header_badge = "SECURITY CHALLENGE"
        title = "Security Verification: OTP Required"
        body = f"Proof-of-delivery flagged for <b>{shipment_id}</b>.<br>Obtain the 6-digit verification code sent via SMS/WhatsApp to <b>{recipient}</b> to release consignment."
        btn_text = "Enter 6-Digit OTP"
        btn_class = "btn-handset-otp"
    else: # PACKAGE_FREEZE or API_CREDENTIAL_REVOKED
        theme_color = "#EF4444"
        header_badge = "EMERGENCY SUSPENSION"
        title = "Session Revoked by SecOps"
        body = f"Kinematic velocity violation detected on consignment <b>{shipment_id}</b> (Cargo: RM {cargo_value:.2f}).<br><br><b>DELIVERY INTERCEPTED BY WARDEN AGENT.</b> Quarantine shipment and report to Section 23 hub."
        btn_text = "Terminal Locked: Contact Dispatch"
        btn_class = "btn-handset-freeze"

    render_html(f"""
<div class="handset-container">
    <div class="handset-notch"></div>
    <div class="handset-screen">
        <div>
            <div class="handset-topbar">
                <span style="display:flex; align-items:center; gap:4px;">{wifi_icon} GDEX-NET</span>
                <span>14:18</span>
                <span style="display:flex; align-items:center; gap:4px;">{battery_icon} 78%</span>
            </div>
            <div style="text-align: center; margin-bottom: 12px;">
                <div style="font-size: 10px; font-weight: 800; color: {theme_color}; letter-spacing: 0.08em; text-transform: uppercase;">
                    [{header_badge}]
                </div>
                <div style="font-size: 14px; font-weight: 800; color: #FFFFFF; margin-top: 3px; letter-spacing:0.02em;">
                    GDEX Courier Go v4.2
                </div>
            </div>
            <div class="handset-card">
                <div style="font-size: 11px; color: #94A3B8;">Active Consignment:</div>
                <div style="font-size: 13px; font-weight: 700; color: #F8FAFC;">{shipment_id}</div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Courier: <b style="color:#CBD5E1;">{courier_name}</b></div>
            </div>
            <div style="background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px; margin-top: 10px;">
                <div style="font-size: 12px; font-weight: 700; color: {theme_color}; margin-bottom: 6px; letter-spacing:0.02em;">
                    {title}
                </div>
                <div style="font-size: 11px; line-height: 1.45; color: #CBD5E1;">
                    {body}
                </div>
            </div>
        </div>
        <div style="margin-top: 16px;">
            <button class="handset-action-btn {btn_class}">
                {btn_text}
            </button>
            <div style="text-align:center; font-size:9px; color:#64748B; margin-top:8px; font-family:'JetBrains Mono', monospace;">
                AegisNode Edge Daemon Connected
            </div>
        </div>
    </div>
</div>
""")
