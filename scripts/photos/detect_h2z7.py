# Fits the screen of h2z7CB0its4 (the hand covers its bottom-right corner, so the
# right and bottom edges are fitted only where the hand is not). Prints the quad.
import cv2, numpy as np, json, sys
# White-screen key: bright and low-saturation (skin is warm and saturated).
path='full/h2z7CB0its4.jpg'; x0,y0,x1,y1=1250,230,1820,1180
im=cv2.imread(path); sub=im[y0:y1,x0:x1].astype(np.float32)
b,g,r=sub[...,0],sub[...,1],sub[...,2]
L=(b+g+r)/3; sat=np.max(sub,2)-np.min(sub,2)
key=((L>170)&(sat<40)).astype(np.uint8)*255
key=cv2.morphologyEx(key,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(key); i=1+np.argmax(st[1:,4]); key=(lab==i).astype(np.uint8)*255
cv2.imwrite('key-h2z.png',key)
cs,_=cv2.findContours(key,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); P=max(cs,key=cv2.contourArea)[:,0,:].astype(float)
def fit(sel):
    q=P[sel].astype(np.float32); vx,vy,cx,cy=cv2.fitLine(q,cv2.DIST_HUBER,0,0.01,0.01).ravel(); return np.array([cx,cy]),np.array([vx,vy])
X,Y=P[:,0],P[:,1]
top=fit((Y<130)&(((X>160)&(X<215))|((X>395)&(X<450))))
left=fit((X<120)&(Y>200)&(Y<700))
right=fit((X>400)&(Y>150)&(Y<420))
bottom=fit((Y>780)&(X>120)&(X<300))
def inter(l1,l2):
    p,r=l1; q,s=l2; t=np.linalg.solve(np.array([r,-s]).T,q-p); return p+t[0]*r
Q=[inter(left,top),inter(top,right),inter(right,bottom),inter(bottom,left)]
Q=[(float(p[0]+x0),float(p[1]+y0)) for p in Q]
vis=im.copy(); cv2.polylines(vis,[np.array(Q,np.int32)],True,(0,0,255),2); cv2.imwrite('vis-h2z.jpg',vis[y0-60:y1+60,x0-60:x1+60])
print(json.dumps(Q))
