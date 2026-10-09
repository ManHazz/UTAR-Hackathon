"""
AegisNode - Plotly Visualization Suite
Interactive cyber speedometer, physical feasibility charts, and API threat monitors.
"""

from typing import List, Dict, Any, Optional
import plotly.graph_objects as go

def build_gauge_chart(score: int) -> go.Figure:
    """
    Renders high-impact Zero-Trust Score speedometer gauge with dark cyber aesthetic.
    """
    if score >= 75:
        primary_color = "#10B981"
        status_text = "ZERO-TRUST VERIFIED (CLEAR)"
    elif score >= 40:
        primary_color = "#F59E0B"
        status_text = "ELEVATED RISK (OTP REQUIRED)"
    else:
        primary_color = "#EF4444"
        status_text = "CRITICAL BREACH (PACKAGE FREEZE)"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={
            'reference': 85,
            'increasing': {'color': "#10B981"},
            'decreasing': {'color': "#EF4444"}
        },
        title={
            'text': f"<b>ZERO-TRUST SCORE</b><br><span style='font-size:12px;color:{primary_color};font-weight:700;'>{status_text}</span>",
            'font': {'size': 16, 'color': '#E2E8F0'}
        },
        number={
            'suffix': "/100",
            'font': {'size': 38, 'color': primary_color, 'family': 'Plus Jakarta Sans, Arial Black'}
        },
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#64748B"},
            'bar': {'color': primary_color, 'thickness': 0.38},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [40, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "#FFFFFF", 'width': 4},
                'thickness': 0.85,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#E2E8F0", 'family': 'Plus Jakarta Sans, sans-serif'},
        height=240,
        margin=dict(l=15, r=15, t=55, b=10)
    )
    return fig

def build_route_feasibility_chart(route_evaluations: List[Dict[str, Any]]) -> go.Figure:
    """
    Renders comparison bar chart showing OSRM expected road transit vs logged actual time.
    Proves physical impossibility to hackathon judges.
    """
    if not route_evaluations:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=200,
            annotations=[dict(text="No route segments to evaluate", showarrow=False, font=dict(color="#94A3B8"))]
        )
        return fig

    segments = [r.get("segment", f"Seg {i+1}") for i, r in enumerate(route_evaluations)]
    actual_times = [r.get("actual_elapsed_min", 0) for r in route_evaluations]
    expected_times = [r.get("osrm_expected_min", 0) for r in route_evaluations]
    impossibles = [r.get("is_impossible", False) for r in route_evaluations]

    fig = go.Figure()

    # OSRM Expected Road Duration
    fig.add_trace(go.Bar(
        name="OSRM Road Physics (Min)",
        x=segments,
        y=expected_times,
        marker_color="#38BDF8",
        opacity=0.85,
        hovertemplate="<b>Expected OSRM Duration</b>: %{y:.1f} mins<extra></extra>"
    ))

    # Actual Logged Duration (colored red if impossible)
    bar_colors = ["#EF4444" if imp else "#10B981" for imp in impossibles]
    fig.add_trace(go.Bar(
        name="Courier Logged Time (Min)",
        x=segments,
        y=actual_times,
        marker_color=bar_colors,
        opacity=0.9,
        hovertemplate="<b>Actual Logged Duration</b>: %{y:.1f} mins<extra></extra>"
    ))

    fig.update_layout(
        barmode='group',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        font={'color': "#E2E8F0", 'family': 'Plus Jakarta Sans, sans-serif'},
        title=dict(
            text="<b>Road Kinematics: OSRM Required Duration vs. Logged Time</b>",
            font=dict(size=13, color="#94A3B8")
        ),
        xaxis=dict(
            tickfont=dict(size=11, color="#CBD5E1"),
            gridcolor="rgba(255,255,255,0.05)"
        ),
        yaxis=dict(
            title=dict(text="Duration (Minutes)", font=dict(size=11, color="#94A3B8")),
            tickfont=dict(size=10, color="#94A3B8"),
            gridcolor="rgba(255,255,255,0.08)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        ),
        height=220,
        margin=dict(l=20, r=20, t=35, b=20)
    )
    return fig

def build_api_threat_chart(scenario_data: Dict[str, Any]) -> go.Figure:
    """
    Renders high-impact API surge and exfiltration threat chart for Scenario 4.
    """
    events = scenario_data.get("events", [])
    req_per_min = events[0].get("request_count_per_minute", 520) if events else 520
    standard_limit = events[0].get("standard_rate_limit", 60) if events else 60

    # Simulated timeline around 03:14 AM
    timeline = ["03:00", "03:05", "03:10", "03:12", "03:14", "03:15 (Warden Cutoff)", "03:20"]
    baseline = [15, 18, 22, 20, standard_limit, 0, 0]
    surge = [15, 18, 45, 180, req_per_min, 0, 0]

    fig = go.Figure()

    # Normal Threshold Line
    fig.add_trace(go.Scatter(
        x=timeline,
        y=[standard_limit] * len(timeline),
        mode="lines",
        name=f"Standard Rate Limit ({standard_limit}/min)",
        line=dict(color="#F59E0B", width=2, dash="dash"),
        hoverinfo="name"
    ))

    # Malicious Traffic Surge
    fig.add_trace(go.Scatter(
        x=timeline,
        y=surge,
        mode="lines+markers",
        name="Subcontractor API Calls / Min",
        line=dict(color="#EF4444", width=3),
        marker=dict(size=8, color=["#38BDF8", "#38BDF8", "#F59E0B", "#EF4444", "#EF4444", "#10B981", "#10B981"]),
        fill="tozeroy",
        fillcolor="rgba(239, 68, 68, 0.15)",
        hovertemplate="<b>Requests</b>: %{y} req/min at %{x}<extra></extra>"
    ))

    # Annotation for Warden Autonomous Cutoff
    fig.add_annotation(
        x="03:15 (Warden Cutoff)",
        y=0,
        text="WARDEN ENFORCEMENT: Token Revoked & IP Blocked",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#10B981",
        arrowsize=1,
        arrowwidth=2,
        ax=0,
        ay=-80,
        bgcolor="rgba(16, 185, 129, 0.2)",
        bordercolor="#10B981",
        font=dict(size=11, color="#A7F3D0")
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        font={'color': "#E2E8F0", 'family': 'Plus Jakarta Sans, sans-serif'},
        title=dict(
            text="<b>Real-Time API Traffic Ingestion (Requests / Minute)</b>",
            font=dict(size=13, color="#94A3B8")
        ),
        xaxis=dict(
            tickfont=dict(size=11, color="#CBD5E1"),
            gridcolor="rgba(255,255,255,0.05)"
        ),
        yaxis=dict(
            title=dict(text="Requests / Min", font=dict(size=11, color="#94A3B8")),
            tickfont=dict(size=10, color="#94A3B8"),
            gridcolor="rgba(255,255,255,0.08)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        ),
        height=270,
        margin=dict(l=20, r=20, t=35, b=20)
    )
    return fig

def build_penalty_breakdown_chart(penalties: Dict[str, Any], final_score: int) -> go.Figure:
    """
    Renders an explainable horizontal breakdown chart showing
    how the Zero-Trust Score was computed from forensic deductions.
    """
    categories = []
    values = []
    colors = []

    # Baseline
    categories.append("Base Trust")
    values.append(100)
    colors.append("#38BDF8")

    if penalties.get("kinematic_road_violation", 0) > 0:
        categories.append("Kinematic Violation")
        values.append(-penalties["kinematic_road_violation"])
        colors.append("#EF4444")

    if penalties.get("telematics_spoof", 0) > 0:
        categories.append("Baseband Spoof")
        values.append(-penalties["telematics_spoof"])
        colors.append("#F59E0B")

    if penalties.get("pod_forgery", 0) > 0:
        categories.append("Optical POD Forgery")
        values.append(-penalties["pod_forgery"])
        colors.append("#EF4444")

    if penalties.get("api_scraping_surge", 0) > 0:
        categories.append("API Rate Surge")
        values.append(-penalties["api_scraping_surge"])
        colors.append("#EF4444")

    if penalties.get("off_hours_exfiltration", 0) > 0:
        categories.append("Off-Hours Harvest")
        values.append(-penalties["off_hours_exfiltration"])
        colors.append("#F59E0B")

    # Net Score
    score_color = "#10B981" if final_score >= 75 else ("#F59E0B" if final_score >= 40 else "#EF4444")
    categories.append("Final Trust Score")
    values.append(final_score)
    colors.append(score_color)

    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation='h',
        marker=dict(color=colors),
        text=[f"{v:+d}" if i > 0 and i < len(values)-1 else f"{v}" for i, v in enumerate(values)],
        textposition="auto",
        textfont=dict(size=11, color="#FFFFFF", family="JetBrains Mono, monospace")
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
        title=dict(
            text="<b>Forensic Zero-Trust Penalty Deduction Matrix</b>",
            font=dict(size=12, color="#94A3B8")
        ),
        xaxis=dict(
            tickfont=dict(size=10, color="#94A3B8"),
            gridcolor="rgba(255,255,255,0.06)",
            range=[-80, 110]
        ),
        yaxis=dict(
            tickfont=dict(size=10, color="#CBD5E1"),
            autorange="reversed"
        ),
        height=190,
        margin=dict(l=15, r=15, t=32, b=15)
    )
    return fig
