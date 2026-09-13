import os
import subprocess
import imageio_ffmpeg
from PIL import Image

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
artifacts_dir = r"C:\Users\kaila\.gemini\antigravity-ide\brain\c0023ccc-e286-4dc5-8196-1a7db8fd7a21"
recordings_dir = r"c:\Users\kaila\OneDrive\Desktop\Projects\FluxWarden-Agentic-AI-Hackathon\docs\recordings"

def get_audio_duration(audio_path):
    cmd = [ffmpeg, "-i", audio_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            part = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = part.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 120.0

def build_demo_2():
    print("[Demo 2] Building adaptive recovery MP4...")
    audio_path = os.path.join(recordings_dir, "demo_2_adaptive_recovery_audio.wav")
    output_mp4 = os.path.join(recordings_dir, "demo_2_adaptive_recovery.mp4")
    dur = get_audio_duration(audio_path)
    fps = 20
    total_frames = int(dur * fps)
    out_w, out_h = 1920, 924

    # 4 distinct visual states matching the 4 quarters of the narration:
    # 1. 0s - 30s: Bad Deployment Injected (74% error rate)
    # 2. 30s - 65s: Rollback fails (red alert pulse), agent enters Replan
    # 3. 65s - 95s: Traffic rerouted to backup-service, 6 verification probes running
    # 4. 95s - 120s: Incident Resolved glowing card and forensic post-mortem
    img_files = [
        os.path.join(artifacts_dir, "demo_running_state_1789318505352.png"),
        os.path.join(artifacts_dir, "demo_running_state_1789318851484.png"),
        os.path.join(artifacts_dir, "demo_started_verification_1789318881451.png"),
        os.path.join(artifacts_dir, "incident_resolved_1789327556960.png")
    ]

    loaded_images = []
    for f in img_files:
        if os.path.exists(f):
            im = Image.open(f).convert("RGB")
            im = im.resize((out_w, out_h), Image.Resampling.LANCZOS)
            loaded_images.append(im.tobytes())
        else:
            print(f"Warning: {f} not found")

    if not loaded_images:
        print("Error: No images found for Demo 2")
        return False

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

    frames_per_stage = total_frames // len(loaded_images)
    for idx, img_bytes in enumerate(loaded_images):
        count = frames_per_stage if idx < len(loaded_images) - 1 else (total_frames - (frames_per_stage * (len(loaded_images) - 1)))
        print(f"  Streaming Stage {idx + 1}/{len(loaded_images)} ({count} frames / {count/fps:.1f}s)...")
        chunk = 100
        for i in range(0, count, chunk):
            batch = min(chunk, count - i)
            proc.stdin.write(img_bytes * batch)

    proc.stdin.close()
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        print(f"[Success] Created {output_mp4} ({os.path.getsize(output_mp4) / 1024 / 1024:.2f} MB)")
        return True
    else:
        print(f"[Error] Demo 2 FFmpeg failed:\n{stderr.decode('utf-8', errors='ignore')[-500:]}")
        return False

def merge_all():
    print("\n[Merging] Combining Demo 1, Demo 2, and Demo 3 into Master Presentation MP4...")
    vid1 = os.path.join(recordings_dir, "demo_1_overview.mp4")
    vid2 = os.path.join(recordings_dir, "demo_2_adaptive_recovery.mp4")
    vid3 = os.path.join(recordings_dir, "demo_3_chaos_approval.mp4")
    master_out = os.path.join(recordings_dir, "fluxwarden_master_demo.mp4")

    if not (os.path.exists(vid1) and os.path.exists(vid2) and os.path.exists(vid3)):
        print("Missing one of the video parts for merging")
        return False

    list_file = os.path.join(recordings_dir, "concat_list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        f.write(f"file '{vid1.replace(os.sep, '/')}'\n")
        f.write(f"file '{vid2.replace(os.sep, '/')}'\n")
        f.write(f"file '{vid3.replace(os.sep, '/')}'\n")

    cmd = [
        ffmpeg, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        master_out
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        size_mb = os.path.getsize(master_out) / 1024 / 1024
        dur = get_audio_duration(master_out)
        print(f"[Master Demo Success] Created {master_out} ({size_mb:.2f} MB, {dur:.1f}s)")
        if os.path.exists(list_file):
            os.remove(list_file)
        return True
    else:
        print(f"[Error] Concat failed:\n{res.stderr[-500:]}")
        return False

if __name__ == "__main__":
    if build_demo_2():
        merge_all()
