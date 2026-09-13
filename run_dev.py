import os
import subprocess
import sys
import time

def main():
    print("=" * 65)
    print("  FLUXWARDEN: Autonomous AI Incident Investigation & Recovery")
    print("  Team: kailashsharma8 | Pochiraju Kailash Ram Markandeya Sharma")
    print("  Hackathon: Agentic AI Hackathon, Tech Zephyr 4.0 | IIT Bhubaneswar")
    print("=" * 65)
    print("\nStarting FluxWarden API Backend on http://localhost:8000 ...")

    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=os.path.join(os.path.dirname(__file__), "apps", "api")
    )

    print("Backend API launched (PID: %d)." % api_process.pid)
    print("Swagger docs available at: http://localhost:8000/docs")
    print("To launch frontend: cd apps/web && npm install && npm run dev")
    print("Press Ctrl+C to terminate.")

    try:
        api_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down FluxWarden...")
        api_process.terminate()

if __name__ == "__main__":
    main()
