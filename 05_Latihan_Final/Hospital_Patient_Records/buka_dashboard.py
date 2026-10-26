"""Script praktis untuk membuka Prototype Smart EHR & Data Quality Dashboard di browser web default.
Dapat dijalankan langsung dengan:
    python3 buka_dashboard.py
"""

import os
import sys
import webbrowser
from pathlib import Path

def main():
    dashboard_path = Path(__file__).resolve().parent / "dashboard.html"
    if not dashboard_path.exists():
        print(f"Error: Berkas {dashboard_path} tidak ditemukan.")
        sys.exit(1)
        
    url = f"file://{dashboard_path.as_posix()}"
    print("=" * 70)
    print(" Prototype Smart EHR & Data Quality Dashboard")
    print(" AI-Powered Co-Pilot & Real-Time Hospital Governance Hub")
    print(" Massachusetts General Hospital (Synthea Dataset Benchmark)")
    print("=" * 70)
    print(f"Membuka dashboard di browser web default...")
    print(f"Path: {dashboard_path}")
    print("=" * 70)
    
    webbrowser.open(url)

if __name__ == "__main__":
    main()
