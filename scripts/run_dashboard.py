#!/usr/bin/env python3
"""
Dashboard Launcher Script

Convenience script to launch the Streamlit dashboard.

Usage:
    python scripts/run_dashboard.py
    # or
    streamlit run app/dashboard.py
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch the Streamlit dashboard"""
    project_root = Path(__file__).parent.parent
    dashboard_path = project_root / "app" / "dashboard.py"
    
    if not dashboard_path.exists():
        print(f"Error: Dashboard file not found at {dashboard_path}")
        sys.exit(1)
    
    print("🚀 Launching Solar Energy Dashboard...")
    print(f"📁 Dashboard location: {dashboard_path}")
    print("\nThe dashboard will open in your default web browser.")
    print("Press Ctrl+C to stop the server.\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(dashboard_path),
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
    except Exception as e:
        print(f"Error launching dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

