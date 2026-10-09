"""
AegisNode - Custom CSS & Styling System
Enterprise-Grade Cyber-Physical SOC Command Center Design System
Strict adherence to Splunk ES / CrowdStrike Falcon / Microsoft Sentinel aesthetic.
Zero emojis - 100% professional enterprise security command aesthetics.
"""

def get_svg_icon(name: str, color: str = "#94A3B8", size: int = 16) -> str:
    """Returns crisp inline SVG vector icons for enterprise SOC display."""
    icons = {
        "shield": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>''',
        "shield-alert": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>''',
        "shield-check": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>''',
        "crosshair": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>''',
        "cpu": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>''',
        "activity": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>''',
        "lock": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>''',
        "camera": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>''',
        "map-pin": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>''',
        "alert-triangle": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>''',
        "check-circle": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>''',
        "phone": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>''',
        "terminal": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>''',
        "eye": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>''',
        "wifi": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>''',
    }
    return icons.get(name, "")

import textwrap
import streamlit as st

def render_html(html_str: str):
    """Safely renders HTML without markdown converting indented lines into code blocks."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def get_custom_css() -> str:
    """
    Returns high-density SOC command center stylesheet.
    Mimics CrowdStrike Falcon, Splunk ES, and Palo Alto Cortex XSOAR.
    """
    return """
<style>
    /* 1. High-Density Enterprise Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #E2E8F0;
    }

    code, kbd, samp, pre, .font-mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .tabular-nums {
        font-variant-numeric: tabular-nums;
        font-family: 'JetBrains Mono', monospace;
    }

    /* 2. Streamlit Root Canvas Overrides (Pure Tactical Dark) */
    .stApp {
        background-color: #080C14 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B101C !important;
        border-right: 1px solid #1A2338 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #94A3B8;
        font-size: 0.85rem;
    }

    /* 3. Streamlit Button Overrides (Tactical Hardware Switch Aesthetics) */
    div[data-testid="stButton"] button {
        background: #0E1626 !important;
        border: 1px solid #1E293B !important;
        border-radius: 6px !important;
        color: #94A3B8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        padding: 9px 12px !important;
        transition: all 0.15s ease-in-out !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.4) !important;
        text-align: left !important;
    }

    div[data-testid="stButton"] button:hover {
        background: #162138 !important;
        border-color: #38BDF8 !important;
        color: #F8FAFC !important;
    }

    /* Active Incident Button Highlight: Deep Midnight Navy + Electric Cyan Accent */
    div[data-testid="stButton"] button[kind="primary"] {
        background: #0C1E38 !important;
        border: 1px solid #38BDF8 !important;
        color: #38BDF8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.25) !important;
    }

    /* 4. Top SOC Navigation & Command Ribbon */
    .command-header {
        background: #0B111F;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 14px 20px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }

    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }

    .brand-subtitle {
        font-size: 0.76rem;
        color: #64748B;
        font-weight: 500;
        margin-top: 2px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .soc-status-group {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }

    .radar-pulse {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 11px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 700;
        color: #10B981;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.04em;
    }

    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6);
        animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
    }

    @keyframes pulse-ring {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
        70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .mitre-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        background: #111827;
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #F87171;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 0.03em;
    }

    /* 5. Situational Awareness & Telemetry Meta Bar */
    .freshness-strip {
        background: #0B101D;
        border: 1px solid #1A2338;
        border-radius: 6px;
        padding: 6px 14px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        font-size: 0.74rem;
        color: #64748B;
        font-family: 'JetBrains Mono', monospace;
    }

    .freshness-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #38BDF8;
        font-weight: 600;
    }

    /* 6. Section Labels */
    .panel-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.82rem;
        font-weight: 700;
        color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 8px;
        padding-bottom: 4px;
        border-bottom: 1px solid #1E293B;
    }

    /* 7. Unified SOC Telemetry Ribbon (Replacing Rainbow Cards) */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0;
        background: #0B111E;
        border: 1px solid #1E293B;
        border-radius: 8px;
        margin-bottom: 16px;
        overflow: hidden;
    }

    @media (max-width: 900px) {
        .kpi-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    .cyber-kpi {
        padding: 12px 16px;
        border-right: 1px solid #1E293B;
        background: transparent;
    }

    .cyber-kpi:last-child {
        border-right: none;
    }

    .kpi-label {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 4px;
    }

    .kpi-value {
        font-size: 1.28rem;
        font-weight: 800;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.1;
    }

    .kpi-delta {
        font-size: 0.70rem;
        font-weight: 600;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
        font-family: 'JetBrains Mono', monospace;
    }

    .delta-green { color: #10B981; }
    .delta-red { color: #EF4444; }
    .delta-amber { color: #F59E0B; }
    .delta-cyan { color: #38BDF8; }

    /* Clean Enterprise Tabs Navigation */
    div[data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #1E293B !important;
        gap: 8px !important;
        padding-bottom: 0px !important;
        margin-bottom: 16px !important;
    }

    button[data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        color: #64748B !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        padding: 10px 16px !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #E2E8F0 !important;
        background: rgba(255, 255, 255, 0.02) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38BDF8 !important;
        border-bottom: 2px solid #38BDF8 !important;
        background: transparent !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: #38BDF8 !important;
    }

    /* Quiet Incident Briefing Card (Contextual Facts) */
    .incident-briefing {
        background: #0B1120;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 18px;
    }

    .briefing-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
        border-bottom: 1px solid #1A2338;
        flex-wrap: wrap;
        gap: 10px;
    }

    .briefing-id-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .briefing-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 700;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 3px 8px;
        border-radius: 4px;
    }

    .briefing-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .briefing-status {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 0.04em;
    }

    .status-freeze {
        color: #F87171;
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.35);
    }

    .status-otp {
        color: #FBBF24;
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    .status-clear {
        color: #34D399;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
    }

    .briefing-meta-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        padding: 12px 0;
        border-bottom: 1px solid #1A2338;
    }

    @media (max-width: 900px) {
        .briefing-meta-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    .meta-item {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }

    .meta-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .meta-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        font-weight: 700;
        color: #E2E8F0;
    }

    .briefing-summary {
        padding-top: 10px;
        font-size: 0.82rem;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* 8. Authoritative Security Scorecard */
    .soc-scorecard {
        background: #0D1322;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .scorecard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        border-bottom: 1px solid #1A2338;
        padding-bottom: 8px;
    }

    .scorecard-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        color: #94A3B8;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .scorecard-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 10px;
        font-size: 0.78rem;
    }

    .scorecard-cell {
        background: #090E19;
        border: 1px solid #1A2338;
        border-radius: 4px;
        padding: 8px 10px;
    }

    .scorecard-cell-label {
        font-size: 0.65rem;
        color: #64748B;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 2px;
    }

    .scorecard-cell-value {
        font-weight: 700;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }

    /* 9. Actionable Enforcement Banners */
    .warden-banner {
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }

    .banner-freeze {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid #EF4444;
    }

    .banner-otp {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid #F59E0B;
    }

    .banner-clear {
        background: rgba(16, 185, 129, 0.10);
        border: 1px solid #10B981;
    }

    .banner-title {
        font-size: 0.88rem;
        font-weight: 800;
        letter-spacing: 0.02em;
        margin-bottom: 2px;
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
    }

    .banner-desc {
        font-size: 0.80rem;
        color: #CBD5E1;
        line-height: 1.4;
    }

    /* 10. SOAR Automated Multi-Agent Pipeline Timeline */
    .soar-timeline {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    .soar-step {
        background: #0B101D;
        border: 1px solid #1A2338;
        border-radius: 6px;
        padding: 12px 14px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .soar-step-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .soar-step-id {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .soar-badge-sentinel { color: #38BDF8; }
    .soar-badge-investigator { color: #818CF8; }
    .soar-badge-warden { color: #F59E0B; }

    .agent-latency-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        background: #111827;
        border: 1px solid #1F2937;
        padding: 2px 7px;
        border-radius: 3px;
        color: #94A3B8;
    }

    .soar-step-body {
        font-size: 0.80rem;
        color: #94A3B8;
        line-height: 1.45;
    }

    /* Backwards compatibility for agent-card */
    .agent-card {
        background: #0B101D;
        border: 1px solid #1A2338;
        border-radius: 6px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }

    .agent-card-sentinel { border-left: 3px solid #38BDF8; }
    .agent-card-investigator { border-left: 3px solid #818CF8; }
    .agent-card-warden-freeze { border-left: 3px solid #EF4444; }
    .agent-card-warden-otp { border-left: 3px solid #F59E0B; }
    .agent-card-warden-clear { border-left: 3px solid #10B981; }

    .agent-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
    }

    .agent-name-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }

    .agent-body {
        font-size: 0.80rem;
        line-height: 1.45;
        color: #CBD5E1;
    }

    /* 11. Courier Mobile Handset Mockup */
    .handset-container {
        background: #060911;
        border: 2px solid #1E293B;
        border-radius: 20px;
        padding: 10px;
        max-width: 300px;
        margin: 0 auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }

    .handset-notch {
        width: 80px;
        height: 10px;
        background: #111827;
        border-radius: 6px;
        margin: 0 auto 8px auto;
    }

    .handset-screen {
        background: #0B101D;
        border-radius: 12px;
        padding: 12px;
        min-height: 340px;
        color: #F8FAFC;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .handset-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.68rem;
        color: #64748B;
        margin-bottom: 10px;
        font-family: 'JetBrains Mono', monospace;
    }

    .handset-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 6px;
        padding: 10px;
        margin-bottom: 8px;
    }

    .handset-action-btn {
        width: 100%;
        padding: 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.80rem;
        text-align: center;
        border: none;
        font-family: 'JetBrains Mono', monospace;
    }

    .btn-handset-success { background: #10B981; color: #FFFFFF; }
    .btn-handset-freeze { background: #EF4444; color: #FFFFFF; }
    .btn-handset-otp { background: #F59E0B; color: #FFFFFF; }

    /* 12. Cryptographic Hash Badge */
    .hash-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        background: #090D18;
        border: 1px solid #1E293B;
        color: #38BDF8;
        padding: 2px 7px;
        border-radius: 3px;
        word-break: break-all;
    }

    /* 13. Dataframe Overrides */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1E293B;
        border-radius: 6px;
        overflow: hidden;
    }

    /* Expander styling */
    div[data-testid="stExpander"] {
        background: #0B101D;
        border: 1px solid #1E293B;
        border-radius: 6px;
    }
</style>
"""
