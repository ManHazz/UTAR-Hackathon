"""
AegisNode - Proof-of-Delivery (POD) Visual Forensics Inspector
Examines courier uploaded photos, AI vision anomaly scores, and EXIF metadata.
Enterprise SOC inspection surface - Zero Emojis.
"""

from typing import Dict, Any
import streamlit as st
from aegisnode.ui.styles import get_svg_icon, render_html

def render_pod_inspector(scenario_data: Dict[str, Any]):
    """
    Renders an interactive forensic viewfinder and EXIF inspection panel
    for courier Proof-of-Delivery photos without raw markdown indentation bugs.
    """
    events = scenario_data.get("events", [])
    last_event = events[-1] if events else {}
    pod = last_event.get("pod_evidence", {})

    if not pod:
        st.info("No Proof-of-Delivery photo submitted for this shipment stage.")
        return

    status = pod.get("photo_status", "UNKNOWN")
    anomaly_score = pod.get("vision_anomaly_score", 0.05 if status == "VALID" else 0.88)
    camera_model = pod.get("exif_camera_model", "Sony IMX890 Mobile Sensor")
    otp_verified = pod.get("otp_verified", False)
    timestamp_match = pod.get("exif_timestamp_match", status == "VALID")

    camera_icon = get_svg_icon("camera", color="#38BDF8", size=15)
    alert_icon = get_svg_icon("alert-triangle", color="#EF4444", size=24)
    check_icon = get_svg_icon("check-circle", color="#10B981", size=24)

    # Styling and preview based on POD validation status
    if status == "FORGED":
        status_bg = "#EF4444"
        image_simulation = f'''<div style="background: radial-gradient(circle, #2D1515 0%, #170A0A 100%); height: 130px; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:8px; border: 1px dashed #EF4444; margin-bottom:12px;"><div>{alert_icon}</div><div style="color:#F87171; font-weight:700; font-size:12px; margin-top:6px; letter-spacing:0.04em;">RECYCLED SCREENSHOT DETECTED</div><div style="color:#94A3B8; font-size:11px;">Car floor mat / duplicated thumbnail artifact</div></div>'''
    elif status == "SUSPICIOUS":
        status_bg = "#F59E0B"
        image_simulation = f'''<div style="background: #0B0F19; height: 130px; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:8px; border: 1px dashed #F59E0B; margin-bottom:12px;"><div>{alert_icon}</div><div style="color:#FBBF24; font-weight:700; font-size:12px; margin-top:6px; letter-spacing:0.04em;">BLACK / COVERED CAMERA SENSOR</div><div style="color:#94A3B8; font-size:11px;">Zero lux ambient illumination detected</div></div>'''
    else:
        status_bg = "#10B981"
        image_simulation = f'''<div style="background: radial-gradient(circle, #064E3B 0%, #022C22 100%); height: 130px; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:8px; border: 1px dashed #10B981; margin-bottom:12px;"><div>{check_icon}</div><div style="color:#6EE7B7; font-weight:700; font-size:12px; margin-top:6px; letter-spacing:0.04em;">RESIDENTIAL GATE AND PARCEL CONFIRMED</div><div style="color:#A7F3D0; font-size:11px;">Visual confirmation at recipient premise</div></div>'''

    risk_color = "#EF4444" if anomaly_score > 0.5 else "#10B981"
    camera_color = "#EF4444" if "Screenshot" in camera_model else "#38BDF8"
    ts_color = "#10B981" if timestamp_match else "#EF4444"
    ts_text = "[MATCH CONFIRMED]" if timestamp_match else "[METADATA MISMATCH]"
    otp_color = "#10B981" if otp_verified else "#F59E0B"
    otp_text = "[OTP VERIFIED]" if otp_verified else "[OTP NOT PROVIDED]"

    # Use render_html to guarantee raw clean HTML rendering
    render_html(f"""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; margin-bottom: 12px;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 10px;">
        <div style="display:flex; align-items:center; gap:8px;">
            {camera_icon}
            <span style="font-size: 12px; font-weight: 700; color: #E2E8F0; text-transform:uppercase; letter-spacing:0.05em;">Optical POD Forensic Inspection</span>
        </div>
        <span style="background:{status_bg}; color:white; font-size:10px; font-weight:800; padding:3px 8px; border-radius:4px; font-family:monospace;">
            [{status}]
        </span>
    </div>
    {image_simulation}
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11px;">
        <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="color: #94A3B8;">AI Vision Anomaly:</div>
            <div style="color: {risk_color}; font-size: 13px; font-weight: 800; margin-top:2px;">{anomaly_score*100:.0f}% Risk Index</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="color: #94A3B8;">EXIF Sensor:</div>
            <div style="color: {camera_color}; font-size: 11px; font-family:monospace; font-weight: 700; margin-top:2px;">{camera_model[:22]}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="color: #94A3B8;">EXIF Timestamp:</div>
            <div style="color: {ts_color}; font-weight: 700; margin-top:2px;">{ts_text}</div>
        </div>
        <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="color: #94A3B8;">Customer Handover OTP:</div>
            <div style="color: {otp_color}; font-weight: 700; margin-top:2px;">{otp_text}</div>
        </div>
    </div>
</div>
""")
