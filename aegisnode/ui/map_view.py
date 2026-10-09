"""
AegisNode - Map View Component
Interactive Folium map for spatial telemetry, waypoints, and kinematic anomalies.
"""

from typing import Dict, Any, List
import folium
from streamlit_folium import st_folium

def render_interactive_map(scenario_data: Dict[str, Any], has_anomaly: bool, height: int = 380):
    """
    Renders an interactive Folium Map centered on Klang Valley delivery points
    using free OpenStreetMap tiles with custom tactical markers.
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

    points: List[List[float]] = []

    for idx, ev in enumerate(events):
        loc = ev.get("location", {})
        pt = [loc.get("lat", 0.0), loc.get("lon", 0.0)]
        points.append(pt)
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

    # Route polyline with tactile styling
    route_color = "#EF4444" if has_anomaly else "#0284C7"
    folium.PolyLine(
        points,
        color=route_color,
        weight=4,
        opacity=0.85,
        dash_array="6, 6" if has_anomaly else None
    ).add_to(m)

    return st_folium(m, height=height, width="100%", returned_objects=[])
