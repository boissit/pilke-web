import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from comp import *
P='full/h2z7CB0its4.jpg'
quad=[(1375.01,314.93),(1739.04,309.20),(1690.18,1115.31),(1318.97,1107.59)]
photo=cv2.cvtColor(cv2.imread(P),cv2.COLOR_BGR2RGB).astype(np.float32)/255
shape=photo.shape[:2]
LANG=lang_arg()
STILL={'fi': 'screens/story.png', 'en': 'screens/story-en.png'}[LANG]
scr=ios_screen(load_still(STILL), 2.164, clock=CLOCK[LANG])
scr.save('screen-story-ios.png')
rgb,rq=warp_screen(scr,quad,shape,0.13)
# Bound: the fitted quad, grown a few pixels, so the photo's own corners decide.
bound=cv2.dilate((rq>0.02).astype(np.uint8),np.ones((9,9),np.uint8)).astype(np.float32)
scol=np.float32([0.925,0.963,0.967]); Ls=scol.mean(); cs=scol/Ls
L=photo.mean(2); c=photo/np.maximum(L,1e-3)[...,None]
dev=np.linalg.norm(c-cs,axis=2)
skin=np.clip((photo[...,0]-photo[...,2]-0.02)/0.12,0,1)
A=np.clip(L/Ls*1.03,0,1)*(1-skin)*bound
near_skin=cv2.GaussianBlur(cv2.dilate((skin>0.3).astype(np.uint8),np.ones((7,7),np.uint8)).astype(np.float32),(0,0),2)
bezel=np.float32([0.045,0.06,0.07])
pure=(A>0.985).astype(np.float32)
shade=masked_blur(photo,pure,8)
lit=rgb*shade
g=estimate_grain(P,(1450,500,1600,650)); print('grain',g)
rng=np.random.default_rng(1); n=cv2.GaussianBlur(rng.normal(0,g,shape).astype(np.float32),(0,0),0.6)*1.5
lit=cv2.GaussianBlur(lit,(0,0),0.55)+n[...,None]
unmix_thumb=photo+A[...,None]*(lit-shade)
unmix_bezel=A[...,None]*lit+(1-A[...,None])*bezel
ring=(A>0.01)&(A<0.99)
w=near_skin[...,None]
out=np.where(ring[...,None], w*unmix_thumb+(1-w)*unmix_bezel, unmix_thumb)
out=np.clip(out,0,1)
save(out,f'ex2-{LANG}-full.jpg',94)
cv2.imwrite('ex2-A.png',(A*255).astype(np.uint8))
