import os
import sys
import subprocess
import json

WORK_DIR = "/Users/junshu/Documents/Obsidian Vault/20_Projects/27_TCC_津カントリー/SwingClub_マニュアル_利用者目線/video_ep02"
SLIDES_DIR = os.path.join(WORK_DIR, "slides")
AUDIO_DIR = os.path.join(WORK_DIR, "audio")
TEMP_DIR = os.path.join(WORK_DIR, "temp_segments")
os.makedirs(TEMP_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(WORK_DIR, "SwingClub_PaperPlay_Ep02_Reservation.mp4")

def get_duration(audio_file):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", audio_file
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(res.stdout)
    return float(data["format"]["duration"])

segments = []
print("Creating video segments for each slide...")

for i in range(1, 7):
    slide_png = os.path.join(SLIDES_DIR, f"slide_{i}.png")
    audio_mp3 = os.path.join(AUDIO_DIR, f"audio_{i}.mp3")
    segment_mp4 = os.path.join(TEMP_DIR, f"seg_{i}.mp4")
    
    dur = get_duration(audio_mp3)
    total_dur = dur + 0.8  # 0.8s padding for natural pause
    
    # Render segment: loop slide image with audio
    # Adding silent audio padding at end
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", slide_png,
        "-i", audio_mp3,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(total_dur),
        segment_mp4
    ]
    subprocess.run(cmd, check=True)
    segments.append(segment_mp4)
    print(f"Segment {i} rendered ({total_dur:.2f}s)")

# Concat segments
concat_list = os.path.join(TEMP_DIR, "concat.txt")
with open(concat_list, "w") as f:
    for seg in segments:
        f.write(f"file '{seg}'\n")

print("Concatenating all segments into final MP4...")
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy",
    OUTPUT_VIDEO
]
subprocess.run(cmd, check=True)

# Also copy to Vault _attachments/ for easy linking
ATTACH_DIR = "/Users/junshu/Documents/Obsidian Vault/_attachments"
os.makedirs(ATTACH_DIR, exist_ok=True)
dest_video = os.path.join(ATTACH_DIR, "SwingClub_PaperPlay_Ep02_Reservation.mp4")
subprocess.run(["cp", OUTPUT_VIDEO, dest_video], check=True)

print(f"Final Video created successfully at: {OUTPUT_VIDEO}")
print(f"Copied to _attachments: {dest_video}")
