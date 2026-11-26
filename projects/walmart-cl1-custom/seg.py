import subprocess, sys
from scenes_all import *
frame, scenes = make_renderer()
a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
cmd = ["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
       "-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p",out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for i in range(a, b):
    p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait(); print("done", a, b)
