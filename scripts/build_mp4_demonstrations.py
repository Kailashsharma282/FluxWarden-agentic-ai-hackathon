import os
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageSequence

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
artifacts_dir = r"C:\Users\kaila\.gemini\antigravity-ide\brain\c0023ccc-e286-4dc5-8196-1a7db8fd7a21"
recordings_dir = r"c:\Users\kaila\OneDrive\Desktop\Projects\FluxWarden-Agentic-AI-Hackathon\docs\recordings"
os.makedirs(recordings_dir, exist_ok=True)

def get_audio_duration(audio_path):
    cmd = [ffmpeg, "-i", audio_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            # Duration: 00:01:41.51,
            part = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = part.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 60.0

def convert_webp_to_mp4(webp_path, audio_path, output_mp4, fps=25):
    print(f"\n[Processing] Converting {os.path.basename(webp_path)} + {os.path.basename(audio_path)} -> {os.path.basename(output_mp4)}")
    im = Image.open(webp_path)
    w, h = im.size
    # Ensure even dimensions for H.264
    out_w = w if w % 2 == 0 else w - 1
    out_h = h if h % 2 == 0 else h - 1

    audio_dur = get_audio_duration(audio_path)
    total_needed_frames = int(audio_dur * fps)
    print(f"Audio duration: {audio_dur:.2f}s | Target frames: {total_needed_frames} at {fps} fps | Dimensions: {out_w}x{out_h}")

    cmd = [
        ffmpeg, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{out_w}x{out_h}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    frame_count = 0
    last_frame_bytes = None

    try:
        for frame in ImageSequence.Iterator(im):
            rgb_frame = frame.convert("RGB")
            if (rgb_frame.width, rgb_frame.height) != (out_w, out_h):
                rgb_frame = rgb_frame.crop((0, 0, out_w, out_h))
            last_frame_bytes = rgb_frame.tobytes()
            proc.stdin.write(last_frame_bytes)
            frame_count += 1
            if frame_count % 300 == 0:
                print(f"  Streamed {frame_count} frames...")

        # If audio is longer than video, hold last frame
        if frame_count < total_needed_frames and last_frame_bytes:
            remaining = total_needed_frames - frame_count
            print(f"  Holding final screen state for remaining {remaining} frames ({remaining/fps:.1f}s)...")
            chunk_size = 100
            for i in range(0, remaining, chunk_size):
                batch = min(chunk_size, remaining - i)
                proc.stdin.write(last_frame_bytes * batch)
            frame_count += remaining

        proc.stdin.close()
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
            out_size = os.path.getsize(output_mp4)
            print(f"[Success] Generated {output_mp4} ({out_size / 1024 / 1024:.2f} MB)")
            return True
        else:
            print(f"[Error] FFmpeg failed with code {proc.returncode}:\n{stderr.decode('utf-8', errors='ignore')[-500:]}")
            return False
    except Exception as e:
        print(f"[Exception] {e}")
        return False

# Part 3: Chaos Lab & Human Approval
webp3 = os.path.join(artifacts_dir, "chaos_approval_demo_1789319107514.webp")
audio3 = os.path.join(recordings_dir, "demo_3_chaos_approval_audio.wav")
out3 = os.path.join(recordings_dir, "demo_3_chaos_approval.mp4")

if os.path.exists(webp3) and os.path.exists(audio3):
    convert_webp_to_mp4(webp3, audio3, out3, fps=20)
