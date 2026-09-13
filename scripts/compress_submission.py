import os
import subprocess
import imageio_ffmpeg
import zipfile

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
root_dir = r"c:\Users\kaila\OneDrive\Desktop\Projects\FluxWarden-Agentic-AI-Hackathon"
recordings_dir = os.path.join(root_dir, "docs", "recordings")
demo_videos_dir = os.path.join(root_dir, "submission", "4_Demo_Videos")
zip_path = os.path.join(root_dir, "FluxWarden_Hackathon_Submission.zip")

os.makedirs(demo_videos_dir, exist_ok=True)

# 1. Optimize MP4 videos using 720p CRF 26 for ultra-crisp quality under 50MB
def optimize_video(input_path, output_path):
    cmd = [
        ffmpeg, "-y",
        "-i", input_path,
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "26",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        output_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        sz = os.path.getsize(output_path) / 1024 / 1024
        print(f"[Optimized] {os.path.basename(output_path)}: {sz:.2f} MB")
        return True
    else:
        print(f"[Error] Failed to optimize {input_path}")
        return False

# Optimize master demo and individual videos into submission/4_Demo_Videos
master_src = os.path.join(recordings_dir, "fluxwarden_master_demo.mp4")
master_dst = os.path.join(demo_videos_dir, "fluxwarden_master_demo.mp4")
optimize_video(master_src, master_dst)

for vname in ["demo_1_overview.mp4", "demo_2_adaptive_recovery.mp4", "demo_3_chaos_approval.mp4"]:
    vsrc = os.path.join(recordings_dir, vname)
    vdst = os.path.join(demo_videos_dir, vname)
    if os.path.exists(vsrc):
        optimize_video(vsrc, vdst)

# 2. Package into FluxWarden_Hackathon_Submission.zip
# Exclude:
# - raw .webp and .wav files (since MP4 has both video + audio embedded)
# - duplicate video files in docs/recordings
# - node_modules, .git, .venv, __pycache__, .pytest_cache, dist, *.db

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

# Exclude .webp, .wav, .pyc, .db to keep zip lightweight and strictly under 50MB
exclude_extensions = {".pyc", ".db", ".sqlite", ".sqlite3", ".log", ".webp", ".wav"}

print(f"\n[Packaging] Building lightweight ZIP ({zip_path})...")

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    # Add root files
    for fname in include_files:
        fpath = os.path.join(root_dir, fname)
        if os.path.exists(fpath):
            arcname = os.path.join("FluxWarden_Hackathon_Submission", fname)
            zipf.write(fpath, arcname)

    # Add directories
    for dname in include_dirs:
        dpath = os.path.join(root_dir, dname)
        if not os.path.exists(dpath):
            continue
        for current_root, dirs, files in os.walk(dpath):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]

            # Avoid duplicate videos: if in docs/recordings, skip MP4s since they are in submission/4_Demo_Videos
            if "docs" in current_root and "recordings" in current_root:
                continue

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

total_mb = os.path.getsize(zip_path) / 1024 / 1024
print(f"\n==================================================")
print(f"FINAL SUBMISSION ZIP SIZE: {total_mb:.2f} MB (Target: < 50 MB)")
print(f"==================================================")
