"""
AegisNode - Map View Component
Interactive Folium map for spatial telemetry, waypoints, and kinematic anomalies.
Renders real road network geometry via OpenStreetMap OSRM graph curves.
"""

from typing import Dict, Any, List
from datetime import datetime
import folium
from streamlit_folium import st_folium

from aegisnode.agents.osrm_service import get_leg_route_geometry, haversine_distance_km

def _parse_timestamp(ts_str: str) -> float:
    try:
        return datetime.fromisoformat(ts_str).timestamp()
    except Exception:
        return 0.0

def render_interactive_map(scenario_data: Dict[str, Any], has_anomaly: bool, height: int = 380):
    """
    Renders an interactive Folium Map centered on Klang Valley delivery points
    using OpenStreetMap tiles with custom tactical markers and real road geometries.
    """
    events = scenario_data.get("events", [])
    if not events or "location" not in events[0]:
        return None

    first_loc = events[0]["location"]
    last_loc = events[-1]["location"]
    mid_lat = (first_loc["lat"] + last_loc["lat"]) / 2
    mid_lon = (first_loc["lon"] + last_loc["lon"]) / 2

    # Map initialization centered on the transit bounding box
    m = folium.Map(
        location=[mid_lat, mid_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # 1. Render realistic road curves or kinematic anomaly jumps between consecutive checkpoints
    for idx in range(len(events) - 1):
        ev_a = events[idx]
        ev_b = events[idx + 1]
        loc_a = ev_a.get("location", {})
        loc_b = ev_b.get("location", {})
        lat_a, lon_a = loc_a.get("lat", 0.0), loc_a.get("lon", 0.0)
        lat_b, lon_b = loc_b.get("lat", 0.0), loc_b.get("lon", 0.0)

        t_a = _parse_timestamp(ev_a.get("timestamp", ""))
        t_b = _parse_timestamp(ev_b.get("timestamp", ""))
        dt_sec = max(t_b - t_a, 1.0)
        dist_km = haversine_distance_km(lat_a, lon_a, lat_b, lon_b)
        calc_speed_kmh = (dist_km / (dt_sec / 3600.0))

        # Check for physically impossible teleportation jump (> 150 km/h in city traffic)
        if calc_speed_kmh > 150.0:
            # Draw the phantom mock location jump chord in bold dashed red
            folium.PolyLine(
                [[lat_a, lon_a], [lat_b, lon_b]],
                color="#EF4444",
                weight=4.5,
                opacity=0.95,
                dash_array="8, 8",
                tooltip=f"ANOMALOUS JUMP: {calc_speed_kmh:.0f} km/h ({dist_km:.1f} km in {dt_sec/60:.1f} min) - Mock Location Spoofing"
            ).add_to(m)

            # Draw theoretical physical road route in faint dashed slate to show required traversal
            road_geom = get_leg_route_geometry(lat_a, lon_a, lat_b, lon_b)
            if road_geom and len(road_geom) > 2:
                folium.PolyLine(
                    road_geom,
                    color="#64748B",
                    weight=2.5,
                    opacity=0.6,
                    dash_array="4, 6",
                    tooltip=f"Theoretical Highway Route via OSRM ({dist_km:.1f} km - Requires ~26 mins driving)"
                ).add_to(m)
        else:
            # Normal physical traversal: trace exact road curves from OSRM
            road_geom = get_leg_route_geometry(lat_a, lon_a, lat_b, lon_b)
            folium.PolyLine(
                road_geom,
                color="#0284C7",
                weight=4,
                opacity=0.85,
                tooltip=f"Verified Road Traversal: Leg #{idx+1} to #{idx+2} ({dist_km:.1f} km @ {calc_speed_kmh:.0f} km/h)"
            ).add_to(m)

    # 2. Render Checkpoint Markers
    for idx, ev in enumerate(events):
        loc = ev.get("location", {})
        pt = [loc.get("lat", 0.0), loc.get("lon", 0.0)]
        seq = ev.get("sequence", idx + 1)
        event_type = ev.get("event_type", "PING")
        speed = ev.get("speed_kmh", 0)
        tower = ev.get("cell_tower_id", "N/A")
        note = ev.get("note", "")
        time_str = ev.get("timestamp", "").split("T")[-1][:5] if "T" in ev.get("timestamp", "") else ""

        is_last = (idx == len(events) - 1)
        
        if is_last and has_anomaly:
            icon = folium.Icon(color="red", icon="warning-sign", prefix="glyphicon")
            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; min-width: 180px;">
                <div style="background:#EF4444; color:white; padding:4px 8px; border-radius:4px; font-weight:bold; margin-bottom:6px;">
                    [ALERT] ANOMALY DETECTED #{seq}
                </div>
                <b>Event:</b> {event_type} ({time_str})<br>
                <b>Location:</b> {loc.get('label', 'Waypoint')}<br>
                <b>Logged Speed:</b> {speed} km/h<br>
                <b>Cell Tower:</b> <span style="font-family:monospace;">{tower}</span><br>
                <i style="color:#DC2626; font-size:11px;">{note}</i>
            </div>
            """
        elif is_last:
            icon = folium.Icon(color="green", icon="ok-sign", prefix="glyphicon")
            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; min-width: 180px;">
                <div style="background:#10B981; color:white; padding:4px 8px; border-radius:4px; font-weight:bold; margin-bottom:6px;">
                    [VERIFIED] DESTINATION REACHED #{seq}
                </div>
                <b>Event:</b> {event_type} ({time_str})<br>
                <b>Location:</b> {loc.get('label', 'Waypoint')}<br>
                <b>Logged Speed:</b> {speed} km/h<br>
                <b>Cell Tower:</b> <span style="font-family:monospace;">{tower}</span>
            </div>
            """
        elif idx == 0:
            icon = folium.Icon(color="blue", icon="home", prefix="glyphicon")
            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; min-width: 180px;">
                <div style="background:#3B82F6; color:white; padding:4px 8px; border-radius:4px; font-weight:bold; margin-bottom:6px;">
                    [ORIGIN] CENTRAL HUB #{seq}
                </div>
                <b>Location:</b> {loc.get('label', 'Origin Hub')}<br>
                <b>Dispatched:</b> {time_str}<br>
                <b>Tower:</b> <span style="font-family:monospace;">{tower}</span>
            </div>
            """
        else:
            icon = folium.Icon(color="cadetblue", icon="record", prefix="glyphicon")
            popup_html = f"""
            <div style="font-family: sans-serif; font-size: 12px; min-width: 180px;">
                <b>Transit Checkpoint #{seq}</b><br>
                <b>Time:</b> {time_str} | <b>Speed:</b> {speed} km/h<br>
                <b>Location:</b> {loc.get('label', 'Waypoint')}<br>
                <b>Cell Tower:</b> <span style="font-family:monospace;">{tower}</span>
            </div>
            """

        folium.Marker(
            pt,
            popup=popup_html,
            tooltip=f"#{seq} {event_type} - {loc.get('label', '')}",
            icon=icon
        ).add_to(m)

    res = st_folium(m, height=height, width="100%", returned_objects=[])
    import streamlit as st
    st.markdown(
        """
        <div style="display:flex; flex-wrap:wrap; gap:16px; font-size:11px; color:#94A3B8; margin-top:4px; padding:4px 8px; background:rgba(15,23,42,0.4); border-radius:6px; border:1px solid rgba(148,163,184,0.15);">
            <span><b style="color:#0284C7;">― Solid Blue:</b> Real Road Graph (OSRM Traversal)</span>
            <span><b style="color:#EF4444;">-- Dashed Red:</b> 458 km/h Spoofed Teleportation Jump</span>
            <span><b style="color:#64748B;">-- Dashed Gray:</b> Highway Traversal Baseline</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    return res
