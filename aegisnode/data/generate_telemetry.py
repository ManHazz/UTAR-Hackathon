"""
AegisNode - Synthetic Telemetry & Evidence Generator
Generates realistic last-mile logistics datasets for GDEX x ANON Hackathon 2026.
Supports normal operations and targeted cybersecurity/fraud threat vectors.
"""

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

DATA_DIR = Path(__file__).parent

def create_normal_delivery() -> dict:
    """Happy path: standard delivery from GDEX Shah Alam Hub to PJ SS2."""
    t0 = datetime(2026, 10, 3, 9, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    return {
        "scenario_id": "SCN-NORMAL-01",
        "scenario_name": "Normal Delivery (Happy Path)",
        "threat_level": "NONE",
        "shipment_id": "GDX-SHP-20261003-081",
        "courier_id": "GDX-081",
        "courier_name": "Muhammad Farhan",
        "courier_vehicle": "Toyota HiAce (BND 4812)",
        "parcel_value_myr": 48.50,
        "parcel_category": "Standard Apparel",
        "recipient_name": "Ahmad Daniyal",
        "delivery_address": "No. 42, Jalan SS 2/64, 47300 Petaling Jaya, Selangor",
        "expected_destination": {"lat": 3.1186, "lon": 101.6214, "label": "Customer Residence, SS2 PJ"},
        "events": [
            {
                "sequence": 1,
                "timestamp": (t0).isoformat(),
                "event_type": "PICKUP",
                "location": {"lat": 3.0738, "lon": 101.5385, "label": "GDEX Central Hub, Shah Alam"},
                "speed_kmh": 0,
                "battery_pct": 98,
                "cell_tower_id": "MY-MAXIS-4102-1",
                "note": "Package sorted and scanned into van"
            },
            {
                "sequence": 2,
                "timestamp": (t0 + timedelta(minutes=18)).isoformat(),
                "event_type": "IN_TRANSIT",
                "location": {"lat": 3.0912, "lon": 101.5794, "label": "Federal Highway near Batu Tiga"},
                "speed_kmh": 62,
                "battery_pct": 94,
                "cell_tower_id": "MY-MAXIS-4102-4",
                "note": "Normal transit traffic flow"
            },
            {
                "sequence": 3,
                "timestamp": (t0 + timedelta(minutes=34)).isoformat(),
                "event_type": "IN_TRANSIT",
                "location": {"lat": 3.1070, "lon": 101.6030, "label": "LDP Highway Exit (Kelana Jaya)"},
                "speed_kmh": 45,
                "battery_pct": 91,
                "cell_tower_id": "MY-CELCOM-5201-9",
                "note": "Approaching neighborhood sector"
            },
            {
                "sequence": 4,
                "timestamp": (t0 + timedelta(minutes=46)).isoformat(),
                "event_type": "DELIVERED",
                "location": {"lat": 3.1186, "lon": 101.6214, "label": "Customer Residence, SS2 PJ"},
                "speed_kmh": 0,
                "battery_pct": 89,
                "cell_tower_id": "MY-CELCOM-5201-2",
                "pod_evidence": {
                    "photo_status": "VALID",
                    "photo_label": "Front Gate with Parcel Box",
                    "exif_timestamp_match": True,
                    "otp_verified": True
                },
                "note": "Recipient acknowledged delivery"
            }
        ]
    }

def create_gps_spoofing() -> dict:
    """Critical attack: 15 km teleportation in 2 minutes (requires >450 km/h)."""
    t0 = datetime(2026, 10, 3, 14, 0, 0, tzinfo=timezone(timedelta(hours=8)))
    return {
        "scenario_id": "SCN-FRAUD-GPS-02",
        "scenario_name": "GPS Teleportation Spoofing (Phantom Courier)",
        "threat_level": "CRITICAL",
        "shipment_id": "GDX-SHP-20261003-042",
        "courier_id": "GDX-042",
        "courier_name": "Kevin Tan",
        "courier_vehicle": "Yamaha NVX 155 (WQL 9021)",
        "parcel_value_myr": 1850.00,
        "parcel_category": "High-Value Consumer Electronics (iPhone 17 Pro)",
        "recipient_name": "Sarah Lim",
        "delivery_address": "Unit 18-03, Menara PJX, Persiaran Barat, 46050 Petaling Jaya",
        "expected_destination": {"lat": 3.1032, "lon": 101.6445, "label": "Menara PJX, Petaling Jaya"},
        "events": [
            {
                "sequence": 1,
                "timestamp": (t0).isoformat(),
                "event_type": "PICKUP",
                "location": {"lat": 3.0738, "lon": 101.5385, "label": "GDEX Central Hub, Shah Alam"},
                "speed_kmh": 0,
                "battery_pct": 82,
                "cell_tower_id": "MY-U-MOBILE-1092",
                "note": "Package scanned out for delivery"
            },
            {
                "sequence": 2,
                "timestamp": (t0 + timedelta(minutes=15)).isoformat(),
                "event_type": "IN_TRANSIT",
                "location": {"lat": 3.0450, "lon": 101.5200, "label": "Shah Alam Section 23 Industrial Park"},
                "speed_kmh": 4,
                "battery_pct": 79,
                "cell_tower_id": "MY-U-MOBILE-1092",
                "note": "Unscheduled stationary delay (11 mins) in industrial warehouse zone"
            },
            {
                "sequence": 3,
                "timestamp": (t0 + timedelta(minutes=17)).isoformat(),
                "event_type": "DELIVERED",
                "location": {"lat": 3.1032, "lon": 101.6445, "label": "Menara PJX, Petaling Jaya"},
                "speed_kmh": 0,
                "battery_pct": 78,
                "cell_tower_id": "MY-U-MOBILE-1092",  # Cell tower DID NOT CHANGE even though GPS jumped 15 km!
                "pod_evidence": {
                    "photo_status": "SUSPICIOUS",
                    "photo_label": "Black screen / obscure angle",
                    "exif_timestamp_match": False,
                    "otp_verified": False
                },
                "note": "Courier app forced delivery mark via mock location provider"
            }
        ]
    }

def create_pod_photo_fraud() -> dict:
    """Evasion attack: Courier at location, but captures fake/replayed POD photo."""
    t0 = datetime(2026, 10, 3, 16, 20, 0, tzinfo=timezone(timedelta(hours=8)))
    return {
        "scenario_id": "SCN-FRAUD-POD-03",
        "scenario_name": "POD Photo Forgery / Recycled Proof Attack",
        "threat_level": "HIGH",
        "shipment_id": "GDX-SHP-20261003-109",
        "courier_id": "GDX-109",
        "courier_name": "Ravi Kumar",
        "courier_vehicle": "Isuzu D-Max (VEE 7711)",
        "parcel_value_myr": 720.00,
        "parcel_category": "Designer Cosmetics & Perfumes",
        "recipient_name": "Nurul Huda",
        "delivery_address": "No. 15, Jalan Maarof, Bangsar, 59100 Kuala Lumpur",
        "expected_destination": {"lat": 3.1319, "lon": 101.6705, "label": "Bangsar Residence, KL"},
        "events": [
            {
                "sequence": 1,
                "timestamp": (t0).isoformat(),
                "event_type": "IN_TRANSIT",
                "location": {"lat": 3.1250, "lon": 101.6620, "label": "Jalan Bangsar Approach"},
                "speed_kmh": 32,
                "battery_pct": 65,
                "cell_tower_id": "MY-DIGI-3301-1",
                "note": "Courier enters Bangsar delivery sector"
            },
            {
                "sequence": 2,
                "timestamp": (t0 + timedelta(minutes=8)).isoformat(),
                "event_type": "DELIVERED",
                "location": {"lat": 3.1319, "lon": 101.6705, "label": "Bangsar Residence, KL"},
                "speed_kmh": 0,
                "battery_pct": 63,
                "cell_tower_id": "MY-DIGI-3301-3",
                "pod_evidence": {
                    "photo_status": "FORGED",
                    "photo_label": "Car floor mat & recycled delivery thumbnail",
                    "vision_anomaly_score": 0.88,
                    "exif_camera_model": "Screenshot_Android_14",
                    "otp_verified": False
                },
                "note": "Physical GPS coordinates match, but visual proof is synthetic/fraudulent"
            }
        ]
    }

def create_api_scraping_attack() -> dict:
    """Cybersecurity attack: 3 AM Subcontractor token credential compromise."""
    t0 = datetime(2026, 10, 3, 3, 14, 22, tzinfo=timezone(timedelta(hours=8)))
    return {
        "scenario_id": "SCN-CYBER-API-04",
        "scenario_name": "Subcontractor API Credential Abuse / Data Exfiltration",
        "threat_level": "CRITICAL",
        "subcontractor_id": "SUB-PARTNER-KLANG-LOGISYNC",
        "courier_name": "LogiSync Partner Fleet #4",
        "courier_vehicle": "Hino 300 Series (BQU 1920)",
        "api_key_prefix": "gdx_live_sub_892f...",
        "source_ip": "185.220.101.44",  # Known offshore VPN/Tor exit
        "user_agent": "python-requests/2.31.0",
        "events": [
            {
                "sequence": 1,
                "timestamp": (t0 - timedelta(minutes=14)).isoformat(),
                "event_type": "DEPOT_STATIONARY",
                "location": {"lat": 3.0333, "lon": 101.4450, "label": "GDEX Klang Partner Terminal (Stationary Fleet)"},
                "speed_kmh": 0,
                "battery_pct": 100,
                "cell_tower_id": "MY-DIGI-4190-KLG",
                "endpoint": "/api/v2/manifests/batch-export",
                "request_count_per_minute": 520,
                "standard_rate_limit": 60,
                "hour_of_day": 3,
                "records_requested": 12500,
                "payload_sensitivity": "Customer Phone, Delivery Address, PII",
                "note": "Fleet stationary in depot while API harvested from external Tor node"
            },
            {
                "sequence": 2,
                "timestamp": (t0).isoformat(),
                "event_type": "LOGISTICS_CORRIDOR",
                "location": {"lat": 3.0010, "lon": 101.3980, "label": "Port Klang Container Hub (Authorized Sector)"},
                "speed_kmh": 0,
                "battery_pct": 98,
                "cell_tower_id": "MY-DIGI-4190-KLG",
                "endpoint": "/api/v2/manifests/batch-export",
                "request_count_per_minute": 520,
                "standard_rate_limit": 60,
                "hour_of_day": 3,
                "records_requested": 12500,
                "payload_sensitivity": "Customer Phone, Delivery Address, PII",
                "note": "Out-of-hours bulk manifest exfiltration detected; credentials revoked at gateway"
            }
        ]
    }

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    scenarios = [
        ("normal_delivery.json", create_normal_delivery()),
        ("fraud_gps_spoof.json", create_gps_spoofing()),
        ("fraud_pod_spoof.json", create_pod_photo_fraud()),
        ("fraud_api_scraping.json", create_api_scraping_attack()),
    ]
    for filename, data in scenarios:
        out_path = DATA_DIR / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[OK] Generated {out_path.name} ({len(json.dumps(data))} bytes)")

if __name__ == "__main__":
    main()
