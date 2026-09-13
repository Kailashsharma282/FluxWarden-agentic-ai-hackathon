import os
import shutil
import zipfile

root_dir = r"c:\Users\kaila\OneDrive\Desktop\Projects\FluxWarden-Agentic-AI-Hackathon"
recordings_dir = os.path.join(root_dir, "docs", "recordings")
demo_videos_dir = os.path.join(root_dir, "submission", "4_Demo_Videos")
zip_path = os.path.join(root_dir, "FluxWarden_Hackathon_Submission.zip")

# 1. Copy MP4 files to submission/4_Demo_Videos
os.makedirs(demo_videos_dir, exist_ok=True)
mp4_files = [
    "fluxwarden_master_demo.mp4",
    "demo_1_overview.mp4",
    "demo_2_adaptive_recovery.mp4",
    "demo_3_chaos_approval.mp4"
]

for f in mp4_files:
    src = os.path.join(recordings_dir, f)
    dst = os.path.join(demo_videos_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {f} ({os.path.getsize(src) / 1024 / 1024:.2f} MB) -> submission/4_Demo_Videos")
    else:
        print(f"Warning: {src} does not exist!")

# 2. Files and directories to include in zip
include_dirs = ["submission", "apps", "docs", "scripts"]
include_files = [
    "README.md",
    "docker-compose.yml",
    "Makefile",
    "render.yaml",
    "vercel.json",
    "run_dev.py",
    ".env.example",
    "pytest.ini"
]

exclude_dirs = {
    "node_modules",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "dist",
    ".tempmediaStorage",
    ".system_generated",
    "build"
}

exclude_extensions = {".pyc", ".db", ".sqlite", ".sqlite3", ".log"}

print(f"\n[Packaging] Creating {zip_path}...")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    # Add root files
    for fname in include_files:
        fpath = os.path.join(root_dir, fname)
        if os.path.exists(fpath):
            arcname = os.path.join("FluxWarden_Hackathon_Submission", fname)
            zipf.write(fpath, arcname)
            print(f"  + Added file: {fname}")

    # Add directories
    for dname in include_dirs:
        dpath = os.path.join(root_dir, dname)
        if not os.path.exists(dpath):
            continue
        for current_root, dirs, files in os.walk(dpath):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in exclude_extensions:
                    continue
                if file.startswith(".env") and not file.endswith(".example"):
                    continue

                full_path = os.path.join(current_root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                arcname = os.path.join("FluxWarden_Hackathon_Submission", rel_path)
                zipf.write(full_path, arcname)

size_mb = os.path.getsize(zip_path) / 1024 / 1024
print(f"\n[Success] Created {zip_path} ({size_mb:.2f} MB)")
