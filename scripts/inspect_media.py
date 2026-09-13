import subprocess
import imageio_ffmpeg
import os

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
recordings_dir = r"c:\Users\kaila\OneDrive\Desktop\Projects\FluxWarden-Agentic-AI-Hackathon\docs\recordings"

files = [
    "demo_1_overview.webp",
    "demo_1_overview_audio.wav",
    "demo_2_adaptive_recovery.webp",
    "demo_2_adaptive_recovery_audio.wav",
    "demo_3_chaos_approval.webp",
    "demo_3_chaos_approval_audio.wav"
]

for f in files:
    path = os.path.join(recordings_dir, f)
    if os.path.exists(path):
        size = os.path.getsize(path)
        cmd = [ffmpeg, "-i", path]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        # Find Duration line in stderr
        dur = "Unknown"
        for line in res.stderr.splitlines():
            if "Duration:" in line or "Video:" in line or "Audio:" in line:
                print(f"[{f}] ({size} bytes) -> {line.strip()}")
    else:
        print(f"[{f}] NOT FOUND!")
