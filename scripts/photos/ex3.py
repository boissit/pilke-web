import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from comp import *
P='full/kljagr9EGSc.jpg'
quad=[(1969.36,2223.74),(2782.31,2234.23),(2780.56,3996.80),(1965.55,4002.80)]
R=float(sys.argv[1]) if len(sys.argv)>1 else 0.105
photo=cv2.cvtColor(cv2.imread(P),cv2.COLOR_BGR2RGB).astype(np.float32)/255
shape=photo.shape[:2]
scr=ios_screen(load_still('screens/date.png'), 2.165, notch_frac=0.56); scr.save('screen-date-ios.png')
rgb,a=warp_screen(scr,quad,shape,R)
a=cv2.GaussianBlur(a,(0,0),0.7)
inside=(a>0.5).astype(np.float32)
L=photo.mean(2); sat=photo.max(2)-photo.min(2)
bg=inside*((L>0.8)&(sat<0.06)).astype(np.float32)
bg=cv2.erode(bg,np.ones((5,5),np.uint8))
base=plane_fit(photo,bg)
ref=np.percentile(photo[bg>0.5],95,axis=0); print('white',ref)
lit=rgb*np.clip(base,0,1)
g=estimate_grain(P,(3500,1000,3800,1300)); print('grain',g)
rng=np.random.default_rng(3); n=cv2.GaussianBlur(rng.normal(0,g,shape).astype(np.float32),(0,0),0.6)*1.5
lit=cv2.GaussianBlur(lit,(0,0),0.7)+n[...,None]
# The photo's own notch: its dark pixels in the top middle of the screen stay.
region=region_mask(quad,shape,(0.2,0.0,0.8,0.06))
dark=np.clip((0.35-L)/0.15,0,1)*region
dark=cv2.GaussianBlur(dark,(0,0),0.6)
A=a*(1-dark)
out=photo*(1-A[...,None])+np.clip(lit,0,1)*A[...,None]
save(np.clip(out,0,1),'ex3-full.jpg',94)
