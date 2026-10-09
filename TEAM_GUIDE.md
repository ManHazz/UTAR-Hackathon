# AegisNode — Teammate Guide & Hackathon Playbook

> **Target Audience:** Team Members (Syarafuddin, Aiman, Anis)  
> **Language:** Simple Technical English  
> **Goal:** Help every team member understand the code, the architecture, and how to confidently present to judges.

---

## 1. The Core Idea in 60 Seconds

Imagine you order an iPhone on Shopee, delivered by GDEX.
* **The Problem:** The driver doesn't actually drive to your house. Instead, the driver sits at a coffee shop, turns on a "Mock GPS" app that tricks their phone into saying *"I am at customer's house"*, snaps a photo of their car steering wheel, and marks the parcel as "Delivered". The driver keeps the iPhone and collects the delivery fee. GDEX loses money and gets angry customer calls.
* **Why this happens:** Current logistics apps operate on **Blind Trust**. If the driver's phone sends GPS coordinates, the server blindly believes it.
* **Our Solution (AegisNode):** We implement **Zero-Trust**: *"Never trust, always verify"*. We cross-check the phone's GPS with 3 independent checks:
  1. **Speed Physics:** Did the phone move faster than a car can drive?
  2. **Cell Tower Reality:** Did the phone's cellular baseband actually connect to new mobile towers along the highway?
  3. **Real Road Maps:** Does OpenStreetMap say this trip is physically possible in the elapsed time?

---

## 2. Meet Our 3 AI Agents (How They Talk to Each Other)

Our system is an **autonomous multi-agent system**. Here is what each agent does:

### Agent 1: Sentinel Agent ("The Watcher")
* **File:** `aegisnode/agents/sentinel_agent.py`
* **Speed:** Extremely fast (runs in ~18 milliseconds).
* **Job:** Watches incoming data streams.
* **What it checks:**
  * Checks velocity between consecutive pings: $v = \Delta \text{distance} / \Delta \text{time}$.
  * Checks cellular tower IDs (`cell_tower_id`). If coordinates jump 15 km from Shah Alam to Petaling Jaya, but the phone is still connected to the Shah Alam cell tower, Sentinel flags `MOCK_LOCATION_SPOOF`.
  * Also watches API traffic at night. If an API key requests 520 calls/minute at 3:00 AM, Sentinel flags `API_RATE_SURGE`.

### Agent 2: Investigator Agent ("The Brain")
* **File:** `aegisnode/agents/investigator_agent.py`
* **Job:** Deep reasoning and physical validation.
* **What it checks:**
  * Calls OpenStreetMap's OSRM routing engine (`osrm_service.py`) to calculate the actual road driving distance on Malaysian roads (Federal Highway, KESAS, etc.).
  * Checks if the delivery photo is suspicious (e.g. car floor mat or screenshot).
  * Computes a **Zero-Trust Score from 0 to 100**:
    * Clean delivery starts at 100.
    * Kinematic violation deducts up to 60 points.
    * Baseband spoofing deducts 35 points.
    * POD photo forgery deducts 40 points.
  * Outputs an explainable deduction list so operators see *exactly* why points were lost.

### Agent 3: Warden Agent ("The Enforcer")
* **File:** `aegisnode/agents/warden_agent.py`
* **Job:** Takes automatic action based on the Trust Score.
* **Actions:**
  * **Score $\ge 75$ (Nominal):** `AUTO_CLEAR`. The package is released and driver payout (+RM 4.50) is approved.
  * **Score $40 - 74$ (Suspicious):** `STEP_UP_CHALLENGE`. The driver cannot finish delivery until they enter a 6-digit OTP code sent directly to the customer's phone.
  * **Score $< 40$ (Critical Fraud):** `PACKAGE_FREEZE`. The courier handset terminal is locked immediately, payout is halted, and SecOps dispatch is alerted.

### The Cryptographic Audit Ledger ("The Black Box")
* **File:** `aegisnode/agents/ledger.py`
* **Job:** Creates an immutable record for our cybersecurity partner **ANON**.
* **How it works:** Every event creates a block containing:
  * Timestamp, agent name, action, and data payload.
  * SHA-256 hash of the current block combined with the previous block's hash.
  * If anyone tries to alter an old block, the entire hash chain breaks. This guarantees **non-repudiation** (proof that cannot be denied in court or arbitration).

---

## 3. How to Run the Project Locally

Before presenting or testing, open PowerShell or Terminal in the project root:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run automated tests (checks that code works 100%)
python -m pytest aegisnode/tests

# 3. Launch dashboard
python -m streamlit run aegisnode/app.py
```

Then open `http://localhost:8501` in your browser.

---

## 4. Live Hackathon Pitch Script (7 Minutes)

Here is a recommended division of speaking roles between teammates:

| Time | Presenter | What to Show on Screen | What to Say (Simple Technical Script) |
| :--- | :--- | :--- | :--- |
| **0:00 - 1:00** | **Pitcher (e.g. Anis)** | Title header on Streamlit dashboard | *"Judges, logistics leaders like GDEX deliver tens of thousands of parcels daily. But traditional apps have a fatal blind spot: Blind Trust in driver phones. Couriers can use fake GPS apps to fake deliveries and steal high-value parcels. We built AegisNode: Zero-Trust Verification for Last-Mile Logistics."* |
| **1:00 - 2:30** | **Demo Lead (e.g. Aiman)** | Click **[CRITICAL] 1. GPS Teleportation** button | *"Let's look at a live incident. Here is a courier carrying an RM 1,850 smartphone. In the map, the courier stops in Shah Alam, and suddenly teleports 15 km to Petaling Jaya in 2 minutes. Our Sentinel Agent flags this immediately: 15 km in 2 minutes requires 450 km/h, and the cell tower connection didn't change!"* |
| **2:30 - 3:45** | **Tech Lead (e.g. Syarafuddin)** | Point to **Investigator Gauge** and **Penalty Chart** | *"Our Investigator Agent queries OpenStreetMap road physics. Driving this route takes 26 minutes on the Federal Highway. The physical feasibility is under 8%. As seen in the deduction chart, Base Trust of 100 drops to 18. Our Warden Agent instantly freezes the parcel, locks the driver's phone, and halts payout."* |
| **3:45 - 5:00** | **Demo Lead (e.g. Aiman)** | Click **[HIGH RISK] 3. Forged POD Photo** and test OTP input | *"What if an issue isn't critical fraud, but suspicious? In Scenario 3, the driver takes a photo of a car mat. Trust Score drops to 50. Instead of shutting down the driver, Warden triggers a Step-Up OTP Challenge. The driver must ask the customer for their 6-digit code. Watch me type `849201` and click Authorize Delivery: the system unseals and approves payout!"* |
| **5:00 - 6:00** | **Tech Lead (e.g. Syarafuddin)** | Scroll to **Cryptographic Audit Ledger** at bottom | *"For our cybersecurity partner ANON: every telemetry ping, agent decision, and supervisor override is sealed into a SHA-256 hash-linked ledger. You can click 'Export Forensic Ledger (JSON)' to download the cryptographic proof for dispute resolution."* |
| **6:00 - 7:00** | **Pitcher (e.g. Anis)** | Click **[NOMINAL] 2. Clean Delivery** | *"In normal deliveries, our system has zero false positives. Trust Score reaches 100, and payout is approved in milliseconds. AegisNode costs RM0 in software licensing and protects GDEX's customer trust. Thank you!"* |

---

## 5. Cheat Sheet: Questions Judges Might Ask & How to Answer

### Q1: "What if the driver loses internet connection in an underground parking lot?"
> **Answer:** *"The Sentinel Agent distinguishes between signal loss and teleportation. When a phone enters a basement, speed is zero and signal drops. In GPS spoofing, the phone actively sends rapid GPS pings claiming to be 15 km away while cell tower IDs remain unchanged. In temporary offline situations, telemetry pings are queued on the handset and verified upon reconnect."*

### Q2: "Why use 3 multi-agents instead of one Python if-else script?"
> **Answer:** *"Specialization and latency. Sentinel is a lightweight scanner running in under 20 milliseconds on every raw ping. We only invoke the heavier Investigator (OSRM road routing and vision checks) when an anomaly is detected. Warden acts as the policy firewall. This multi-agent separation ensures GDEX servers aren't overwhelmed handling tens of thousands of drivers simultaneously."*

### Q3: "Does this cost GDEX a lot of money to run?"
> **Answer:** *"No, the entire stack runs on open-source, free technologies: OpenStreetMap OSRM routing, Streamlit, Python, and local cryptographic hashing. It costs RM 0.00 in proprietary licensing fees, but can save GDEX hundreds of thousands of Ringgit in stolen parcel claims."*

### Q4: "How does the Cryptographic Ledger prevent tampering?"
> **Answer:** *"Each record contains the SHA-256 hash of the previous record. If a compromised insider or hacker tries to modify an old entry (e.g., trying to erase a GPS teleportation alert), the hash of that block changes, breaking the chain for all subsequent blocks. The ledger also exports a JSON proof verifying non-repudiation."*

---

## 6. File-by-File Code Map

If a judge asks to see specific code:

| What the Judge Wants to See | Where to Go |
| :--- | :--- |
| **Main Dashboard & UI** | `aegisnode/app.py` |
| **Velocity & Cell Tower Scanner** | `aegisnode/agents/sentinel_agent.py` |
| **Road Travel Math & Trust Score** | `aegisnode/agents/investigator_agent.py` |
| **OpenStreetMap Kinematics** | `aegisnode/agents/osrm_service.py` |
| **Automated Policy Enforcement** | `aegisnode/agents/warden_agent.py` |
| **SHA-256 Audit Hash Chain** | `aegisnode/agents/ledger.py` |
| **Charts & Visualizations** | `aegisnode/ui/charts.py` |
| **Interactive Map** | `aegisnode/ui/map_view.py` |
| **Mobile Phone Handset Mockup** | `aegisnode/ui/handset_simulator.py` |
| **Automated Pytest Tests** | `aegisnode/tests/test_agents.py` & `test_ui.py` |
