# Wi‑Fi Connection Test Scripts (Windows)

This project provides **Python scripts for testing Wi‑Fi authentication behavior on Windows systems**
using the native `netsh wlan` interface.

The scripts dynamically generate temporary Wi‑Fi profiles (XML format), attempt to connect to a specified SSID, and optionally verify real internet connectivity via ICMP ping.

> ⚠️ **Important Notice**  
> This project is intended **only for educational, testing, or administrative purposes** on networks you **own or are explicitly authorized to manage**.  
> **The author does not assume any responsibility for misuse, damage, or illegal use of this software.**  
> Users are solely responsible for ensuring compliance with **local laws and regulations**.
---

## Project Structure

This repository contains **two separate scripts**, each implementing a different authentication testing strategy.

### Dictionary Mode

**File:** `dictionary.py`

- The user specifies the **target Wi‑Fi SSID** at the beginning of the script
- Candidate passwords are read from a local file named `passwords.txt`
- Passwords are tested **sequentially**, one at a time

This mode simulates a **dictionary‑based authentication test**, commonly used in defensive security research to evaluate password strength against known wordlists.

---

### Bruteforce Mode

**File:** `bruteforce.py`

- The user specifies:
  - **Target Wi‑Fi SSID**
  - **Character set** used for password generation  
    (example: `abcdefghijklmnopqrstuvwxyz,.`)
  - **Minimum password length**
  - **Maximum password length**
- Passwords are generated dynamically based on these parameters and tested sequentially

This mode demonstrates how **bruteforce password generation** works within controlled constraints for academic and research purposes.

---

## Features

- Uses Windows native `netsh wlan` commands
- Dynamically generates temporary WLAN XML profiles
- Supports dictionary‑based and bruteforce‑based testing
- Verifies **actual internet connectivity**, not just Wi‑Fi association
- Automatically cleans up temporary profile files
- No third‑party Python libraries required

---

## Requirements

- **Operating System:** Windows
- **Python:** 3.7+
- **Permissions:** Administrator privileges may be required
- **Network Type:** WPA2‑PSK (AES)

---

## How It Works (High Level)

1. The script reads or generates candidate passwords
2. For each password:
   - A temporary WLAN XML profile is created
   - The profile is added via `netsh wlan`
   - A connection attempt is made to the specified SSID
   - Internet connectivity is verified using an ICMP ping
3. Temporary files are removed after each attempt

> Windows does **not** allow passing Wi‑Fi credentials directly via the command line.  
> For this reason, the use of XML WLAN profiles is required.

---

## Disclaimer

This software is provided **“as is”**, without warranty of any kind.

The author **explicitly disclaims any liability** for:
- Unauthorized access attempts
- Network disruption
- Legal consequences arising from misuse

Use this project **only on networks you own or have explicit permission to test**.
