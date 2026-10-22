"""Script praktis untuk membuka Dashboard Visualisasi Wholesale Customers di browser web default.
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
    print("=" * 65)
    print(" Wholesale Customers Sales Intelligence Dashboard")
    print("=" * 65)
    print(f"Membuka dashboard di browser web default...")
    print(f"Path: {dashboard_path}")
    print("=" * 65)
    
    webbrowser.open(url)

if __name__ == "__main__":
    main()
