"""
AegisNode - Custom CSS & Styling System
Provides Cyber-Physical SOC command center aesthetics, dark glassmorphism,
pulse animations, SVG vector icons, and enterprise UX component styling.
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
    """Returns CSS string injected into the Streamlit dashboard."""
    return """
<style>
    /* Google Fonts Import for high-precision cyber & display typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Tabular numeric alignment for timestamps, metrics, coordinates */
    .tabular-nums {
        font-variant-numeric: tabular-nums;
    }

    /* Command Center Top Header */
    .command-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }

    .brand-title {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #F8FAFC;
    }

    .brand-subtitle {
        font-size: 0.82rem;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 3px;
        letter-spacing: 0.01em;
    }

    /* Freshness & Situational Awareness Bar */
    .freshness-strip {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 8px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        font-size: 0.78rem;
        color: #94A3B8;
    }

    .freshness-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #10B981;
        font-weight: 700;
        letter-spacing: 0.04em;
    }

    /* Live Surveillance Radar Pulse */
    .radar-pulse {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #10B981;
        letter-spacing: 0.04em;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
    }

    @keyframes pulse-ring {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Partner Badge Group */
    .partner-badges {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .partner-pill {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .pill-gdex {
        background: rgba(229, 57, 53, 0.15);
        color: #FF6B6B;
        border: 1px solid rgba(229, 57, 53, 0.3);
    }

    .pill-anon {
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .pill-utar {
        background: rgba(245, 158, 11, 0.15);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* MITRE ATT&CK Classification Badge */
    .mitre-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #F87171;
        padding: 3px 8px;
        border-radius: 4px;
        letter-spacing: 0.03em;
    }

    /* Cyber KPI Metric Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
        margin-bottom: 20px;
    }

    .cyber-kpi {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 14px 16px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .cyber-kpi:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.18);
    }

    .cyber-kpi::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
    }

    .kpi-emerald::before { background: linear-gradient(90deg, #10B981, #34D399); }
    .kpi-amber::before { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
    .kpi-crimson::before { background: linear-gradient(90deg, #EF4444, #F87171); }
    .kpi-cyan::before { background: linear-gradient(90deg, #06B6D4, #38BDF8); }
    .kpi-purple::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }

    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: #F8FAFC;
        font-variant-numeric: tabular-nums;
        line-height: 1.1;
    }

    .kpi-delta {
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .delta-green { color: #10B981; }
    .delta-red { color: #EF4444; }
    .delta-amber { color: #F59E0B; }

    /* Tactical Agent Pipeline Cards */
    .agent-deck {
        margin-top: 14px;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .agent-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 16px 20px;
        position: relative;
        transition: all 0.25s ease;
    }

    .agent-card-sentinel {
        border-left: 4px solid #06B6D4;
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.07) 0%, rgba(15, 23, 42, 0.6) 100%);
    }

    .agent-card-investigator {
        border-left: 4px solid #8B5CF6;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.07) 0%, rgba(15, 23, 42, 0.6) 100%);
    }

    .agent-card-warden-freeze {
        border-left: 4px solid #EF4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(15, 23, 42, 0.7) 100%);
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.12);
    }

    .agent-card-warden-otp {
        border-left: 4px solid #F59E0B;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.09) 0%, rgba(15, 23, 42, 0.7) 100%);
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.1);
    }

    .agent-card-warden-clear {
        border-left: 4px solid #10B981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.08);
    }

    .agent-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }

    .agent-name-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 0.95rem;
        color: #F8FAFC;
    }

    .agent-latency-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2px 8px;
        border-radius: 4px;
        color: #94A3B8;
    }

    .agent-body {
        font-size: 0.88rem;
        line-height: 1.55;
        color: #CBD5E1;
    }

    /* Risk & Enforcement Banners */
    .warden-banner {
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start;
        gap: 14px;
    }

    .banner-freeze {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.22) 0%, rgba(185, 28, 28, 0.15) 100%);
        border: 1px solid #EF4444;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.2);
    }

    .banner-otp {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(180, 83, 9, 0.15) 100%);
        border: 1px solid #F59E0B;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.18);
    }

    .banner-clear {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(4, 120, 87, 0.12) 100%);
        border: 1px solid #10B981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
    }

    .banner-title {
        font-size: 0.98rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        margin-bottom: 4px;
        color: #FFFFFF;
    }

    .banner-desc {
        font-size: 0.85rem;
        color: #E2E8F0;
        line-height: 1.45;
    }

    /* Human-in-the-Loop Override Panel */
    .override-panel {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 14px;
    }

    .override-header {
        font-size: 0.85rem;
        font-weight: 700;
        color: #E2E8F0;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }

    /* Cryptographic Hash Badge */
    .hash-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.25);
        color: #38BDF8;
        padding: 3px 8px;
        border-radius: 4px;
        word-break: break-all;
    }

    /* Courier Mobile Handset Mockup */
    .handset-container {
        background: #090D16;
        border: 2px solid #334155;
        border-radius: 28px;
        padding: 14px;
        max-width: 320px;
        margin: 0 auto;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05);
    }

    .handset-notch {
        width: 100px;
        height: 14px;
        background: #1E293B;
        border-radius: 8px;
        margin: 0 auto 10px auto;
    }

    .handset-screen {
        background: #111827;
        border-radius: 18px;
        padding: 16px 14px;
        min-height: 380px;
        color: #F8FAFC;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .handset-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.7rem;
        color: #94A3B8;
        margin-bottom: 12px;
        font-weight: 600;
    }

    .handset-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .handset-action-btn {
        width: 100%;
        padding: 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        text-align: center;
        border: none;
        cursor: pointer;
    }

    .btn-handset-success {
        background: #10B981;
        color: #FFFFFF;
    }

    .btn-handset-freeze {
        background: #EF4444;
        color: #FFFFFF;
        cursor: not-allowed;
    }

    .btn-handset-otp {
        background: #F59E0B;
        color: #FFFFFF;
    }

    /* Streamlit overrides for seamless clean dark aesthetics */
    div[data-testid="stMetricValue"] {
        font-variant-numeric: tabular-nums;
    }

    /* Clean tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 8px;
        padding: 4px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.82rem;
        color: #94A3B8;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(30, 41, 59, 0.9) !important;
        color: #F8FAFC !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
</style>
"""
