import math
import pathlib
import subprocess
import sys

FPS = 30
CHUNK = 660


def duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", str(path)
    ], text=True).strip()
    return float(out)


def main():
    voice = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("voiceover.mp3")
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path("out/chapter-1.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    dur = duration(voice)
    total = math.ceil(dur * FPS)
    parts = []
    for start in range(0, total, CHUNK):
        end = min(total, start + CHUNK)
        part = out.parent / f"segment-{start:06d}.mp4"
        parts.append(part)
        if not part.exists():
            subprocess.run([sys.executable, "seg.py", str(start), str(end), str(part)], check=True)
    concat = out.parent / "concat.txt"
    concat.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in parts), encoding="utf-8")
    silent = out.parent / "video-only.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(voice),
        "-map", "0:v:0", "-map", "1:a:0", "-t", f"{dur:.3f}",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)
    ], check=True)
    print(f"rendered={out} duration={dur:.3f}s frames={total} segments={len(parts)}")


if __name__ == "__main__":
    main()
