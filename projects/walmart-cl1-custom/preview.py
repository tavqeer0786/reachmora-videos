import sys, time
from scenes_all import *
frame, scenes = make_renderer()
ts = [float(x) for x in sys.argv[2:]]
t0=time.time()
ims=[Image.fromarray(frame(t)).resize((640,360), Image.LANCZOS) for t in ts]
cols=3; rows=(len(ims)+cols-1)//cols
sh=Image.new('RGB',(640*cols,360*rows))
for i,im in enumerate(ims): sh.paste(im,((i%cols)*640,(i//cols)*360))
sh.save(sys.argv[1]); print('ok',time.time()-t0)
