import os
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageSequence

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
artifacts_dir = r"C:\Users\kaila\.gemini\antigravity-ide\brain\c0023ccc-e286-4dc5-8196-1a7db8fd7a21"
recordings_dir = r"c:\Users\kaila\OneDrive\Desktop\Projects\FluxWarden-Agentic-AI-Hackathon\docs\recordings"
demo_videos_dir = r"c:\Users\kaila\OneDrive\Desktop\Projects\FluxWarden-Agentic-AI-Hackathon\submission\4_Demo_Videos"

webp3 = os.path.join(artifacts_dir, "chaos_approval_demo_1789319107514.webp")
audio3 = os.path.join(recordings_dir, "demo_3_chaos_approval_audio.wav")
output_mp4 = os.path.join(demo_videos_dir, "demo_3_chaos_approval.mp4")

# Re-encode demo 3 directly to 720p MP4
im = Image.open(webp3)
fps = 20
out_w, out_h = 1280, 720

cmd = [
    ffmpeg, "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{out_w}x{out_h}",
    "-pix_fmt", "rgb24",
    "-r", str(fps),
    "-i", "-",
    "-i", audio3,
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "26",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "128k",
    "-shortest",
    output_mp4
]

proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

count = 0
last_bytes = None
# Stream first 1760 frames (88 seconds)
max_frames = 1764

for frame in ImageSequence.Iterator(im):
    rgb = frame.convert("RGB").resize((out_w, out_h), Image.Resampling.BILINEAR)
    last_bytes = rgb.tobytes()
    proc.stdin.write(last_bytes)
    count += 1
    if count >= max_frames:
        break

if count < max_frames and last_bytes:
    proc.stdin.write(last_bytes * (max_frames - count))

proc.stdin.close()
stdout, stderr = proc.communicate()

if proc.returncode == 0:
    sz = os.path.getsize(output_mp4) / 1024 / 1024
    print(f"[Success] Rebuilt demo_3_chaos_approval.mp4: {sz:.2f} MB")
else:
    print("Error:", stderr.decode("utf-8", errors="ignore")[-400:])
