# Bob-QA Gatekeeper

![EU AI Act Compliant](https://img.shields.io/badge/EU%20AI%20Act-Compliant-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![IBM Hackathon](https://img.shields.io/badge/Built%20for-IBM%20Hackathon-purple)

---

## 1. The Corporate Problem Statement

In 2026, enterprises are facing an unprecedented challenge due to the hyper-generation of AI-assisted software. Tools like IBM Bob exponentially accelerate code writing, but this massive volume has overwhelmed the cognitive capabilities of Quality Assurance (QA) teams. Senior engineers are bombarded with up to 100,000 lines of synthetic code per hour, trapped in alert fatigue due to thousands of security false positives.

This operational chaos coincides with the enforcement of the **European Union Artificial Intelligence Act (EU AI Act)**, which mandatorily and strictly requires that any algorithmic or AI-generated software classified as "high risk" must have **demonstrable and qualified human oversight** before deployment. Failure to comply with this requirement exposes corporations to fines of up to 35 million euros or 7% of their global annual turnover.

## 2. The Solution: Bob-QA Gatekeeper

**Bob-QA Gatekeeper** is an audit, governance, and regulatory compliance panel developed in Flask and SQLite. It acts as an isolation middleware or "smart tollgate" between the AI-assisted development environment (IBM Bob IDE) and the final deployment pipeline (Production/CI-CD).

The program intercepts machine-generated code **asynchronously**, classifies it based on its regulatory risk level, and freezes its execution. The tool provides a clean interface for a human reviewer to analyze, comment, and sign off on sensitive code blocks, automatically generating an **immutable audit trail** ready for legal inspections.

---

## 3. Architecture and Core Features

The system is structured under a clean, modular pattern that separates data logic, server processing, and the auditor interface, highlighting three main features that make it an *Enterprise-grade* product:

### A. Data Layer and Immutability (`setup_db.py` / `models/`)
Uses a forensic audit-oriented relational database. Every time an AI generates code, the table stores:
* `code_snippet`: The exact code block under suspicion.
* `ai_risk_score`: A mathematical index (0.0 to 1.0) that measures the code's sensitivity.
* Legal accountability fields (`human_approved`, `reviewer_name`, `timestamp`).

### B. Server Engine and Proactive Auto-Solutions (`app.py` / `routes/`)
The backend provides an asynchronous pipeline that prevents slowing down the programmer's pace:
* **Capture and Governance Endpoint:** Receives code functions in the background. The developer's workflow is not interrupted.
* **AI-Driven Resolutive Auto-Corrector:** Unlike a passive blocker, when the system detects high-risk code, the internal AI **automatically generates multiple options of safe, corrected code**. It displays the exact percentage of risk improvement, allowing the auditor to apply the solution directly with a single click. *Gatekeeper doesn't slow down development; it accelerates it securely.*

### C. Ergonomic and Global Dashboard (`templates/` / `static/`)
A web interface optimized for rapid global decision-making:
* **Visual Fatigue Reduction (Apple-Inspired Minimalist Dark Theme):** The interface uses a dark mode design with *glassmorphism* that isn't just aesthetic. It is ergonomically and psychologically designed to mitigate visual fatigue for auditors reading code 8 hours a day, improving their focus and dramatically reducing human error.
* **Corporate Internationalization (i18n):** The system features instant, reactive translation (English/Spanish). It is ready to be deployed immediately in multinational corporations with globally distributed teams.
* **Evidence Export Module:** Instantly generates a downloadable report that constitutes an immutable legal shield against EU regulators.

---

## 4. Real-Time Operational Flow

1. **Generation:** A developer uses IBM Bob IDE to write a critical module.
2. **Submission and Isolation:** Upon saving, the integration module automatically sends the code to the *Bob-QA Gatekeeper* API. It is marked as `Pending`.
3. **Continuity:** The developer continues coding in their IDE; there are no bottlenecks or blocks in their productivity.
4. **Resolutive Auditing:** The QA engineer opens the Dashboard. If it's a high-risk alert, **Gatekeeper offers them already-corrected code options**. The human reviews, accepts the AI's suggestion, adds technical comments, and clicks **"Approve"**.
5. **Deployment and Logging:** The state changes to `Approved`, the code is released to the CI/CD branch, and the audit log is permanently sealed with the reviewer's name.

---

## 5. Why this is a winning solution for the IBM Hackathon

* **Strategic Alignment:** Resolves the biggest current fear of any global IBM client's board of directors: cybersecurity holes injected by synthetic code and severe EU AI Act penalties.
* **Optimal Use of Bob:** Demonstrates how to coordinate and govern the immense speed of IBM Bob, turning a potentially chaotic automation tool into a secure, enterprise-grade environment.
* **Real Business Viability:** It's not a technical toy; it's a functional AI Governance software product that any bank, healthcare entity, or government contractor would buy in 2026 to protect their operations.

---

## Quick Start (Technical Installation)

### Prerequisites
* Python 3.8 or higher

### Installation

1. **Clone the repository and install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database**
   ```bash
   python setup_db.py
   ```
   *This will create the SQLite database and add sample records for the hackathon demonstration.*

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the Panel**
   Open your web browser and go to: `http://localhost:5000`

---
**Built for EU AI Act Compliance - IBM Hackathon**