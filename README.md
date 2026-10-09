# AegisNode: Zero-Trust Defense for Last-Mile Logistics

> **GDEX x ANON x UTAR Agentic AI Cybersecurity Hackathon 2026**  
> **Track:** Secure Logistics & Digital Trust  
> **Team:** Syarafuddin, Aiman, Anis  
> **Tech Stack Cost:** RM 0.00 (100% Free Open-Source Stack)

---

## 1. What is AegisNode?

Logistics companies like **GDEX** deliver tens of thousands of parcels across Malaysia every day. Today, these delivery systems work on **Blind Trust**:
* If a delivery driver's phone says *"I am at the customer's house"*, the system believes it.
* If a driver uploads a photo as Proof-of-Delivery (POD), the system accepts it.

Because of this blind trust, fraud happens:
1. **GPS Teleportation (Ghost Deliveries):** Dishonest couriers use fake GPS apps to mark parcels as "Delivered" from their couch, then steal the high-value goods.
2. **Forged Proof-of-Delivery:** Drivers upload photos of car floor mats, dark corners, or screenshots instead of real customer handovers.
3. **Subcontractor API Credential Theft:** Stolen partner API keys scrape customer names, phone numbers, and addresses late at night (e.g. at 3:00 AM).

**AegisNode** solves this by applying the **Zero-Trust Cybersecurity Framework ("Never Trust, Always Verify")** to physical logistics using an autonomous multi-agent pipeline.

---

## 2. How AegisNode Works: The 3 AI Agents

Instead of a single rigid rule, AegisNode uses **three specialized AI agents** that work together in real time:

```
[ Incoming Courier GPS & POD Data ]
                 │
                 ▼
┌─────────────────────────────────┐
│     1. Sentinel Agent (Watcher) │ ➔ Scans GPS speed & cell tower connections in milliseconds
└────────────────┬────────────────┘
                 │ (Flags Anomaly)
                 ▼
┌─────────────────────────────────┐
│ 2. Investigator Agent (Brain)   │ ➔ Checks road travel physics (OSRM) & POD photo heuristics
└────────────────┬────────────────┘
                 │ (Produces Zero-Trust Score: 0 - 100)
                 ▼
┌─────────────────────────────────┐
│     3. Warden Agent (Enforcer)  │ ➔ Executes automatic, risk-based containment actions
└────────────────┬────────────────┘
                 │
      ┌──────────┴──────────┐
      ▼                     ▼                     ▼
[ Score >= 75 ]       [ Score 40-74 ]       [ Score < 40 ]
  AUTO-CLEAR          STEP-UP OTP           PACKAGE FREEZE
  Payout approved     SMS sent to customer  Quarantine & lock app

                 │
                 ▼
┌─────────────────────────────────┐
│   Cryptographic Audit Ledger    │ ➔ Stores every step into SHA-256 tamper-evident hash chain
└─────────────────────────────────┘
```

### The 3 Core Agents Explained Simply:
1. **Sentinel Agent (The Fast Watcher):**
   * Computes speed between GPS pings.
   * If a courier jumps 15 km in 2 minutes, it requires 450 km/h. Sentinel immediately catches this.
   * Checks cellular baseband ID. If GPS coordinates jump 15 km but the phone is still connected to the same cell tower in Shah Alam, mock GPS spoofing is confirmed.
2. **Investigator Agent (The Deep Brain):**
   * Connects to OpenStreetMap (OSRM) road routing engine.
   * It asks: *"How long does a car actually take to drive this road in Petaling Jaya?"*
   * Analyzes Proof-of-Delivery photos and checks parcel value (smartphones vs low-value items).
   * Computes an **Explainable Zero-Trust Score from 0 to 100** with a detailed penalty deduction breakdown.
3. **Warden Agent (The Policy Enforcer):**
   * Takes immediate action without human bottleneck:
     * **Green (Score $\ge 75$):** Auto-clears delivery and approves driver commission (+RM 4.50).
     * **Amber (Score $40 - 74$):** Demands a 6-digit OTP code sent directly to the customer's phone before the driver can release the parcel.
     * **Red (Score $< 40$):** Instantly freezes the parcel, locks the driver's handset app, and alerts SecOps dispatch.
4. **Cryptographic Audit Ledger (ANON Security Core):**
   * Uses forward-linked **SHA-256 cryptographic hashing** (like a blockchain ledger).
   * Guarantees **non-repudiation**: neither a rogue courier nor a compromised dispatcher can alter the audit log after an incident.

---

## 3. How to Run the Project (3 Simple Steps)

### Step 1: Install Requirements
Make sure you have Python 3.10+ installed. Open terminal / PowerShell and run:
```bash
pip install -r requirements.txt
```

### Step 2: Run Automated Tests
Verify that all agents and UI components are working properly:
```bash
python -m pytest aegisnode/tests
```
*(All 15 automated unit and UI tests should pass with green status.)*

### Step 3: Launch the Command Center Dashboard
```bash
python -m streamlit run aegisnode/app.py
```
Open your web browser at: **`http://localhost:8501`**

---

## 4. The 4 Live Incident Scenarios Ready to Demo

In the dashboard, you can test 4 realistic situations with 1 click:

| Scenario | Incident Type | Trust Score | Warden Enforcement Action |
| :--- | :--- | :---: | :--- |
| **1. GPS Teleportation** | Phantom Courier jumps 15 km in 2 min | **18 / 100** (Red) | **Package Freeze:** Handset app locked, courier payout halted. |
| **2. Clean Delivery** | Legitimate courier route in Subang Jaya | **100 / 100** (Green) | **Auto-Clear:** Verified delivery, payout +RM 4.50 approved. |
| **3. Forged POD Photo** | Courier photographed car floor mat | **50 / 100** (Amber) | **Step-Up OTP:** App requires 6-digit customer SMS code (`849201`). |
| **4. API Exfiltration** | Third-party partner scraping 12,500 PII records at 3:14 AM | **12 / 100** (Red) | **Token Revocation:** Gateway API token revoked, IP blacklisted in WAF. |

---

## 5. Project Folder Structure

```
UTAR-Hackathon/
├── aegisnode/
│   ├── app.py                      # Main Streamlit SOC Command Center dashboard
│   ├── agents/
│   │   ├── sentinel_agent.py       # Agent 1: Fast velocity & cell tower scanner
│   │   ├── investigator_agent.py   # Agent 2: OSRM road physics & trust score reasoner
│   │   ├── warden_agent.py         # Agent 3: Risk-adaptive policy enforcer
│   │   ├── ledger.py               # SHA-256 cryptographic non-repudiation ledger
│   │   ├── orchestrator.py         # Orchestrates the 3-agent pipeline
│   │   └── osrm_service.py         # OpenStreetMap road kinematics calculator
│   ├── data/
│   │   ├── fraud_gps_spoof.json    # Scenario 1 data (GPS teleportation)
│   │   ├── normal_delivery.json    # Scenario 2 data (Clean delivery)
│   │   ├── fraud_pod_spoof.json    # Scenario 3 data (Forged photo)
│   │   ├── fraud_api_scraping.json # Scenario 4 data (3 AM API scraping)
│   │   └── generate_telemetry.py   # Telemetry simulation generator
│   ├── ui/
│   │   ├── styles.py               # Enterprise cyber-physical dark CSS & SVG icons
│   │   ├── charts.py               # Plotly trust gauge, penalty waterfall & radar charts
│   │   ├── map_view.py             # Interactive Folium map with route telemetry
│   │   ├── pod_viewer.py           # Optical proof-of-delivery inspector
│   │   ├── handset_simulator.py    # Courier mobile phone handset mockup
│   │   └── ledger_view.py          # Tamper-evident ledger & JSON export
│   └── tests/
│       ├── test_agents.py          # Unit tests for agents & cryptographic ledger
│       └── test_ui.py              # Unit tests for charts & styles
├── PROJECT_PROPOSAL.md             # Complete academic proposal, citations & methodology
├── TEAM_GUIDE.md                   # Complete guide for teammates & pitch playbook
├── requirements.txt                # Project dependencies (Streamlit, Folium, Plotly, etc.)
└── README.md                       # Main project documentation
```

---

## 6. Teammate & Presentation Resources

* Read **[`PROJECT_PROPOSAL.md`](./PROJECT_PROPOSAL.md)** for the complete academic proposal report, literature review, APA 7th citations, and mathematical formulas.
* Read **[`TEAM_GUIDE.md`](./TEAM_GUIDE.md)** for:
  * Simple explanation of how each teammate can speak during the hackathon pitch.
  * 7-Minute presentation script with exact cue times.
  * Anticipated judge questions and simple technical answers.
