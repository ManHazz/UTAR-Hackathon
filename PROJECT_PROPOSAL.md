# AEGISNODE: ZERO-TRUST VERIFICATION FOR LAST-MILE LOGISTICS
## Technical Report & Project Proposal
**Hackathon:** GDEX x ANON x UTAR Agentic AI Cybersecurity Hackathon 2026  
**Track:** Secure Logistics & Digital Trust  
**Team Members:** Syarafuddin, Aiman, Anis  
**Institution:** Universiti Tunku Abdul Rahman (UTAR)  

---

## TABLE OF CONTENTS
- [1. Introduction](#1-introduction)
  - [1.1 Background of Last-Mile Logistics in Malaysia](#11-background-of-last-mile-logistics-in-malaysia)
  - [1.2 Problem Statements](#12-problem-statements)
  - [1.3 Aims and Objectives](#13-aims-and-objectives)
  - [1.4 Scope and Limitations](#14-scope-and-limitations)
  - [1.5 Significance of the Project](#15-significance-of-the-project)
- [2. Literature Review & Industry Background](#2-literature-review--industry-background)
  - [2.1 The Vulnerability of Client-Side Telematics in Gig Logistics](#21-the-vulnerability-of-client-side-telematics-in-gig-logistics)
  - [2.2 Telematics Evasion: Mock Location Apps & Baseband Discrepancies](#22-telematics-evasion-mock-location-apps--baseband-discrepancies)
  - [2.3 Proof-of-Delivery (POD) Auditing: Optical Heuristic Verification](#23-proof-of-delivery-pod-auditing-optical-heuristic-verification)
  - [2.4 Autonomous Multi-Agent Systems (MAS) in Incident Response](#24-autonomous-multi-agent-systems-mas-in-incident-response)
  - [2.5 Cryptographic Hash Chaining and Merkle Trees for Non-Repudiation](#25-cryptographic-hash-chaining-and-merkle-trees-for-non-repudiation)
  - [2.6 Comparative Analysis of Existing Solutions vs. AegisNode](#26-comparative-analysis-of-existing-solutions-vs-aegisnode)
- [3. Methodology & System Architecture](#3-methodology--system-architecture)
  - [3.1 Overall System Architecture & Data Flow](#31-overall-system-architecture--data-flow)
  - [3.2 The Multi-Agent Roles](#32-the-multi-agent-roles)
  - [3.3 Mathematical Formulations & Heuristic Scoring](#33-mathematical-formulations--heuristic-scoring)
  - [3.4 Threat Simulation Scenarios](#34-threat-simulation-scenarios)
  - [3.5 Technology Stack & RM 0.00 Cost Breakdown](#35-technology-stack--rm-000-cost-breakdown)
- [4. Results, Demonstration & Benchmarks](#4-results-demonstration--benchmarks)
  - [4.1 Security Operations Command Center (SOC) Implementation](#41-security-operations-command-center-soc-implementation)
  - [4.2 Multi-Agent Latency & Processing Performance](#42-multi-agent-latency--processing-performance)
  - [4.3 Automated Test Suite & Coverage Verification](#43-automated-test-suite--coverage-verification)
- [5. Conclusion & Recommendations](#5-conclusion--recommendations)
  - [5.1 Summary of Contributions](#51-summary-of-contributions)
  - [5.2 Real-World Feasibility for GDEX Deployment](#52-real-world-feasibility-for-gdex-deployment)
  - [5.3 Future Work](#53-future-work)

---

## 1. INTRODUCTION

### 1.1 Background of Last-Mile Logistics in Malaysia
The e-commerce economy in Malaysia has grown rapidly, driven by platforms such as Shopee, Lazada, and TikTok Shop. Logistics operators like GDEX move tens of thousands of consignments daily across dense urban networks in the Klang Valley. 

However, the "last-mile" — the final leg of transit from the local distribution hub to the customer's doorstep — remains the most vulnerable and costly segment of the supply chain, accounting for up to 53% of overall shipping expenses. Traditional dispatch platforms operate on **Blind Trust**, meaning servers automatically trust whatever telemetry data is transmitted from couriers' personal smartphones once the driver logs in.

### 1.2 Problem Statements

#### 1.2.1 Blind Trust in Mobile Endpoint Devices
Because logistics apps run on drivers' consumer Android smartphones, dishonest couriers can use free third-party "Mock Location" and GPS spoofing applications. A courier can remain stationary in Shah Alam while artificially broadcasting GPS coordinates in Petaling Jaya, allowing them to falsely mark deliveries as complete without driving the route.

#### 1.2.2 The "Photo & Run" Optical Proof-of-Delivery Loophole
To verify drop-offs, standard apps require drivers to upload a photo. In practice, dishonest drivers snap photos of car floor mats, dark corners, or closed gates, mark the order as complete, and take the item. The system accepts any uploaded image without verifying whether an actual handover took place.

#### 1.2.3 Dispute Deadlock and Lack of Cryptographic Non-Repudiation
When high-value parcels (e.g., consumer electronics worth RM 1,500+) go missing, GDEX is caught in a deadlock: the customer denies receiving the package, while the driver claims delivery took place. Standard database logs lack cryptographic integrity; they can be contested or manipulated, forcing courier companies to absorb significant insurance claims or damage their commercial reputations.

#### 1.2.4 Out-of-Hours Subcontractor API Harvesting
Third-party logistics (3PL) partners and subcontractors hold API credentials to pull delivery manifests. Rogue actors or compromised keys can execute automated batch queries at 3:00 AM, harvesting thousands of customer names, phone numbers, and home addresses for scam operations (such as Cash-on-Delivery fraud).

### 1.3 Aims and Objectives
The primary aim of AegisNode is to replace Blind Trust with a **Zero-Trust Cybersecurity Architecture** for last-mile logistics. Specific objectives include:
1. Develop an autonomous multi-agent pipeline (Sentinel, Investigator, Warden) to analyze incoming telematics within sub-second latencies.
2. Cross-reference GPS coordinates with OpenStreetMap (OSRM) road kinematics and cellular baseband IDs to detect mock-location spoofing.
3. Replace binary pass/fail outcomes with a risk-adaptive policy engine that triggers dynamic Step-Up OTP challenges for borderline anomalies.
4. Build a tamper-evident SHA-256 cryptographic audit ledger to guarantee non-repudiation for dispute resolution.

#### 1.3.1 Research & Engineering Questions
* **RQ1:** Can spatial-temporal road kinematics reliably detect location spoofing without draining the courier's phone battery?
* **RQ2:** How does multi-agent specialization (Sentinel -> Investigator -> Warden) balance verification throughput against deep reasoning latency?
* **RQ3:** Can cryptographic hash chaining establish tamper-evident proof that eliminates delivery dispute deadlocks?

### 1.4 Scope and Limitations
* **Geographical Scope:** Urban road networks of the Klang Valley (Petaling Jaya, Subang Jaya, Shah Alam, Kuala Lumpur).
* **Target Threats:** GPS teleportation/spoofing, optical proof-of-delivery forgery, and out-of-hours API manifest scraping.
* **Architecture:** Streamlit-based Security Operations Command Center (SOC) integrating real-time telemetry simulators, OpenStreetMap OSRM routing, and an internal SHA-256 ledger.

### 1.5 Significance of the Project
* **For GDEX:** Protects high-value cargo, halts fraudulent driver payouts, reduces insurance claim expenses, and eliminates customer dispute deadlocks.
* **For ANON:** Implements genuine Zero-Trust security principles ("Never Trust, Always Verify") and SHA-256 cryptographic non-repudiation mapped to MITRE ATT&CK techniques (`T1056`, `T1566`, `T1114`).
* **Cost Efficiency:** Built on a **100% free open-source stack (RM 0.00 licensing costs)**, allowing immediate enterprise adoption.

---

## 2. LITERATURE REVIEW & INDUSTRY BACKGROUND

### 2.1 The Vulnerability of Client-Side Telematics in Gig Logistics
In gig-economy courier models, drivers are often paid per successful drop (RM 3.50 – RM 5.00 per parcel). This economic structure creates incentives to exploit mobile applications. Because mobile operating systems give users root and developer access, device-side GPS signals cannot be inherently trusted.

### 2.2 Telematics Evasion: Mock Location Apps & Baseband Discrepancies
Android provides a native `ACCESS_MOCK_LOCATION` framework intended for app development, but it is frequently abused by gig workers. When a driver spoofs their GPS coordinates across town, their actual physical device remains connected to the same local cellular tower. Cross-referencing GPS data against the device's cellular baseband tower ID reveals the discrepancy.

### 2.3 Proof-of-Delivery (POD) Auditing: Optical Heuristic Verification
According to the Malaysian Communications and Multimedia Commission (MCMC) *C&M Industry Performance Report*, thousands of consumer complaints are lodged annually regarding disputed and non-delivered parcels. Manual review of delivery photos is operationally impossible for tens of thousands of daily parcels. Automated heuristic verification—analyzing visual entropy, lighting conditions, and metadata—allows suspicious submissions to be flagged immediately.

### 2.4 Autonomous Multi-Agent Systems (MAS) in Incident Response
Traditional cybersecurity relies on monolithic rules that produce high false-positive rates. In an Agentic AI architecture, specialized agents perform distinct tasks:
* Fast sensory scanning (millisecond-scale filtering).
* Deep forensic reasoning (spatial and physical calculations).
* Policy execution (dynamic, risk-adjusted countermeasures).

### 2.5 Cryptographic Hash Chaining and Merkle Trees for Non-Repudiation
To achieve legal non-repudiation, logs must be immutable. By forward-linking records using SHA-256 hashes ($H_n = \text{SHA256}(H_{n-1} + \text{Payload}_n)$), any post-incident alteration invalidates all subsequent hashes, providing clear proof of tampering.

### 2.6 Comparative Analysis of Existing Solutions vs. AegisNode

| Feature / Dimension | Standard Logistics App | Centralized Database Logs | AegisNode Zero-Trust Engine |
| :--- | :---: | :---: | :---: |
| **Trust Model** | Blind Trust | Post-Incident Audit | Zero-Trust (Continuous Verification) |
| **GPS Verification** | Coordinates only | Geofence bounding box | Road kinematics (OSRM) + Baseband ID |
| **POD Inspection** | File upload check | Random manual spot checks | Automated optical entropy heuristics |
| **Policy Response** | Binary (Success/Fail) | Manual ticket creation | Risk-Adaptive (Auto-Clear / OTP / Freeze) |
| **Audit Integrity** | Mutable SQL records | Standard access logs | SHA-256 cryptographic hash chain |
| **Software Cost** | Proprietary SaaS | High database license | **RM 0.00 (Open-Source)** |

---

## 3. METHODOLOGY & SYSTEM ARCHITECTURE

### 3.1 Overall System Architecture & Data Flow
AegisNode processes telematics through a 3-agent pipeline supported by an immutable audit ledger:

```
[ Telemetry Ingestion: GPS / Cell Tower / POD / API Streams ]
                          │
                          ▼
            ┌───────────────────────────┐
            │       SENTINEL AGENT      │ (Velocity & Baseband Scanner)
            └─────────────┬─────────────┘
                          │ [Flags Anomaly]
                          ▼
            ┌───────────────────────────┐
            │     INVESTIGATOR AGENT    │ (OSRM Road Physics & Trust Score)
            └─────────────┬─────────────┘
                          │ [Trust Score: 0 - 100]
                          ▼
            ┌───────────────────────────┐
            │        WARDEN AGENT       │ (Risk-Adaptive Policy Enforcer)
            └──────┬──────┬──────┬──────┘
                   │      │      │
       ┌───────────┘      │      └───────────┐
       ▼                  ▼                  ▼
[Score >= 75]       [Score 40-74]      [Score < 40]
 AUTO-CLEAR          STEP-UP OTP        PACKAGE FREEZE
 Payout Approved     SMS to Customer    Handset Locked & SOC Alert
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ▼
            ┌───────────────────────────┐
            │ CRYPTOGRAPHIC AUDIT LEDGER│ (SHA-256 Non-Repudiation Chain)
            └───────────────────────────┘
```

### 3.2 The Multi-Agent Roles

#### 1. Sentinel Agent (Watcher)
* Runs fast checks across incoming pings (~18ms latency).
* Flags velocities that exceed vehicle physical limits.
* Detects cellular tower mismatches (GPS coordinates moving while the cell tower remains stationary).
* Detects off-hours API request spikes.

#### 2. Investigator Agent (Deep Reasoner)
* Queries OpenStreetMap OSRM routing to obtain real-world driving times along actual roads (e.g., Federal Highway).
* Evaluates photo heuristics and applies risk multipliers for high-value cargo (e.g., smartphones > RM 1,000).
* Calculates an **Explainable Zero-Trust Score (0 to 100)** with a clear penalty breakdown.

#### 3. Warden Agent (Policy Enforcer)
* Executes risk-adaptive countermeasures:
  * **Score >= 75 (Nominal):** Approves delivery and driver payout (+RM 4.50).
  * **Score 40 - 74 (Elevated Risk):** Halts delivery until the driver enters a 6-digit OTP code sent directly to the customer.
  * **Score < 40 (Critical Risk):** Instantly freezes the parcel, locks the courier handset app, and notifies SecOps dispatch.

#### 4. Cryptographic Audit Ledger
* Implements forward-linked SHA-256 hashing.
* Provides one-click JSON export for non-repudiation audit verification.

### 3.3 Mathematical Formulations & Heuristic Scoring

#### 1. Kinematic Velocity Check
Given two consecutive telematics points $P_1(\text{lat}_1, \text{lon}_1, t_1)$ and $P_2(\text{lat}_2, \text{lon}_2, t_2)$:
$$\text{Speed } (v) = \frac{\text{Haversine Distance}(P_1, P_2)}{\Delta t}$$
If $v > 120\text{ km/h}$ within an urban zone, the kinematic penalty is triggered.

#### 2. OSRM Road Feasibility Ratio
$$\text{Feasibility Ratio } (R) = \frac{\text{Actual Elapsed Time}}{\text{OSRM Expected Driving Time}}$$
If $R < 0.25$ (meaning the trip occurred in less than a quarter of the minimum possible driving time), a heavy kinematic violation penalty (-60 points) is deducted.

### 3.4 Threat Simulation Scenarios

| Scenario | Incident Type | Trust Score | Warden Enforcement Action |
| :--- | :--- | :---: | :--- |
| **1. GPS Teleportation** | Phantom Courier jumps 15 km in 2 min | **18 / 100** (Red) | **Package Freeze:** Handset app locked, courier payout halted. |
| **2. Clean Delivery** | Legitimate courier route in Subang Jaya | **100 / 100** (Green) | **Auto-Clear:** Verified delivery, payout +RM 4.50 approved. |
| **3. Forged POD Photo** | Courier photographed car floor mat | **50 / 100** (Amber) | **Step-Up OTP:** App requires 6-digit customer SMS code (`849201`). |
| **4. API Exfiltration** | Third-party partner scraping 12,500 PII records at 3:14 AM | **12 / 100** (Red) | **Token Revocation:** Gateway API token revoked, IP blacklisted in WAF. |

### 3.5 Technology Stack & RM 0.00 Cost Breakdown
* **Framework:** Python 3.10+, Streamlit (Web Command Center), Pandas, Plotly (Interactive visual analytics).
* **Spatial & Kinematics:** Folium (Leaflet maps), OpenStreetMap OSRM Routing Engine (Free public routing API).
* **Cryptography:** Python `hashlib` (SHA-256 forward-linked block hash chaining).
* **Total Software Licensing Cost:** **RM 0.00**.

---

## 4. RESULTS, DEMONSTRATION & BENCHMARKS

### 4.1 Security Operations Command Center (SOC) Implementation
The AegisNode command center was built using Streamlit, Plotly, and Folium. Key capabilities include:
1. **Split-Screen Cyber-Physical Layout:** Interactive spatial map with telemetry logs on the left; Trust Score gauge and agent decision logs on the right.
2. **Forensic Penalty Breakdown Chart:** Visualizes exact deductions (Base Trust 100 -> Kinematic Violation -60 -> Baseband Spoof -35 -> Net Score 5).
3. **Interactive Step-Up Challenge:** Allows operators to input a customer OTP (`849201`) to demonstrate real-time clearance and payout approval.
4. **Courier Handset Preview:** Real-time mobile mockup showing the driver's screen (Verified, Security Challenge, or Emergency Suspension).

### 4.2 Multi-Agent Latency & Processing Performance
* **Sentinel Ingestion Latency:** ~18 ms
* **Investigator Reasoning Latency:** ~142 ms
* **Warden Enforcement Latency:** ~8 ms
* **Total End-to-End Decision Time:** **< 170 ms** (well within real-time logistics SLA requirements).

### 4.3 Automated Test Suite & Coverage Verification
The codebase includes 12 automated unit tests across agent logic, cryptographic integrity, and UI components:
```text
============================= 12 passed in 4.67s ==============================
```

---

## 5. CONCLUSION & RECOMMENDATIONS

### 5.1 Summary of Contributions
AegisNode demonstrates that the **Zero-Trust Cybersecurity Framework** can be applied to physical logistics at **RM 0.00 software cost**. By combining lightweight sensory scanning, spatial road physics, risk-adaptive enforcement, and cryptographic audit ledgers, AegisNode protects couriers, customers, and operators alike.

### 5.2 Real-World Feasibility for GDEX Deployment
AegisNode is designed for modular integration into GDEX's existing driver mobile apps via a lightweight SDK, with backend verification running on standard containerized cloud or on-premise infrastructure.

### 5.3 Future Work
1. **On-Device Edge AI:** Deploy lightweight visual models directly to courier handsets to verify POD photos offline before upload.
2. **Public L2 Blockchain Anchoring:** Periodically anchor the SHA-256 Merkle root to a public blockchain (e.g., Base or Arbitrum) for public non-repudiation.
