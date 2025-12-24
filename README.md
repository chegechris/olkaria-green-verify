# Olkaria Green-Verify: Digital Traceability & Carbon Audit System

## Executive Summary
Olkaria Green-Verify is a backend infrastructure designed to secure the supply chain of Green Ammonia produced at the Olkaria Geothermal Complex. It provides Anti-Counterfeit Verification via USSD and generates immutable Carbon Credit Audit Logs (MRV) for compliance with Gold Standard/Verra.

## Current Status: Alpha Prototype (v0.1)

### Tech Stack
- **Backend:** Python (Flask)
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Interface:** USSD (Africa's Talking Gateway)
- **Infrastructure:** Heroku / Docker

## Core Modules
1. **Anti-Counterfeit Verification**
   - **USSD Gateway:** Handles real-time verification requests from farmers (low-latency).
   - **Ledger Service:** Manages the lifecycle of digital codes (Generated -> Active -> Retired).
2. **Audit Engine:** Logs timestamps and geo-metadata for Carbon Credit verification.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/olkaria-green-verify.git

# Install dependencies
pip install -r requirements.txt

# Run local server
python app.py
```

## 🔒 Security
- Codes are 12-bit cryptographically secure strings.
- Rate limiting applied to prevent brute-force attacks on the USSD endpoint.