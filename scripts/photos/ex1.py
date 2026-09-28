import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from comp import *
P='full/Ebb8fe-NZtM.jpg'
quad=[(1351.51,1428.89),(2266.16,1442.33),(2044.57,3364.03),(1156.96,3253.59)]
R=float(sys.argv[1]) if len(sys.argv)>1 else 0.06
photo=cv2.cvtColor(cv2.imread(P),cv2.COLOR_BGR2RGB).astype(np.float32)/255
shape=photo.shape[:2]
scr=android_screen(load_still('screens/treffit.png'), 2.056); scr.save('screen-treffit-s9.png')
rgb,a=warp_screen(scr,quad,shape,R)
a=cv2.GaussianBlur(a,(0,0),0.7)
inside=(a>0.5).astype(np.float32)
L=photo.mean(2); sat=photo.max(2)-photo.min(2)
bg=inside*((L>0.72)&(sat<0.09)).astype(np.float32)
bg=cv2.erode(bg,np.ones((5,5),np.uint8))
shade=masked_blur(photo,bg,22)
# Normalise by the bright part of the background: the device's white.
ref=np.percentile(shade[bg>0.5],97,axis=0); print('white',ref)
shade=shade/ref*ref.mean()*0.99
shade=shade*(ref/ref.mean())**0.6   # keep most of the cast (the photo is slightly lavender)
lit=rgb*shade
g=estimate_grain(P,(200,3700,500,3900)); print('grain',g)
rng=np.random.default_rng(2); n=cv2.GaussianBlur(rng.normal(0,g,shape).astype(np.float32),(0,0),0.6)*1.5
lit=cv2.GaussianBlur(lit,(0,0),0.7)+n[...,None]
out=photo*(1-a[...,None])+np.clip(lit,0,1)*a[...,None]
save(np.clip(out,0,1),'ex1-full.jpg',94)
