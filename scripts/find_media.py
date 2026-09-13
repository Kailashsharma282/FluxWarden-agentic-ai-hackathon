import os

artifacts_dir = r"C:\Users\kaila\.gemini\antigravity-ide\brain\c0023ccc-e286-4dc5-8196-1a7db8fd7a21"

for root, dirs, files in os.walk(artifacts_dir):
    for f in files:
        if f.endswith(".png") or f.endswith(".webp") or f.endswith(".wav") or f.endswith(".mp4"):
            p = os.path.join(root, f)
            print(f"{os.path.relpath(p, artifacts_dir)}: {os.path.getsize(p)} bytes")
