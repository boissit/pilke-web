import cv2, numpy as np, sys, json
def fit_quad(path, roi, thr=None, out=None):
    im = cv2.imread(path); x0,y0,x1,y1 = roi
    sub = im[y0:y1, x0:x1]
    g = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    if thr is None:
        thr,_ = cv2.threshold(g,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    m = (g > thr).astype(np.uint8)*255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    n,lab,stats,_ = cv2.connectedComponentsWithStats(m)
    i = 1+np.argmax(stats[1:,cv2.CC_STAT_AREA]); m = (lab==i).astype(np.uint8)*255
    cs,_ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull = cv2.convexHull(max(cs,key=cv2.contourArea))
    # densify hull
    pts=[]; h=hull[:,0,:].astype(float)
    for a,b in zip(h, np.roll(h,-1,0)):
        k=max(2,int(np.hypot(*(b-a))))
        pts.append(a+(b-a)*np.linspace(0,1,k,endpoint=False)[:,None])
    P=np.vstack(pts)
    rect=cv2.minAreaRect(P.astype(np.float32)); box=cv2.boxPoints(rect)
    # order box TL,TR,BR,BL
    s=box.sum(1); d=box[:,0]-box[:,1]
    TL=box[np.argmin(s)]; BR=box[np.argmax(s)]; TR=box[np.argmax(d)]; BL=box[np.argmin(d)]
    corners=[TL,TR,BR,BL]; lines=[]
    for a,b in zip(corners, corners[1:]+corners[:1]):
        v=b-a; L=np.hypot(*v); u=v/L; nrm=np.array([-u[1],u[0]])
        t=(P-a)@u; dist=(P-a)@nrm
        sel=(t>0.18*L)&(t<0.82*L)&(np.abs(dist)<0.06*L+15)
        q=P[sel].astype(np.float32)
        vx,vy,cx,cy=cv2.fitLine(q,cv2.DIST_HUBER,0,0.01,0.01).ravel()
        lines.append((np.array([cx,cy]),np.array([vx,vy])))
    def inter(l1,l2):
        p,r=l1; q,s=l2; A=np.array([r,-s]).T; t=np.linalg.solve(A,q-p); return p+t[0]*r
    Q=[inter(lines[3],lines[0]),inter(lines[0],lines[1]),inter(lines[1],lines[2]),inter(lines[2],lines[3])]
    Q=[(float(p[0]+x0),float(p[1]+y0)) for p in Q]
    if out:
        vis=im.copy(); cv2.polylines(vis,[np.array(Q,np.int32)],True,(0,0,255),3)
        cv2.imwrite(out, vis[y0-100:y1+100, x0-100:x1+100])
    return Q, float(thr)
if __name__=='__main__':
    path=sys.argv[1]; roi=list(map(int,sys.argv[2].split(','))); thr=float(sys.argv[3]) if len(sys.argv)>3 and sys.argv[3]!='-' else None
    Q,t=fit_quad(path,roi,thr,sys.argv[4] if len(sys.argv)>4 else None); print(json.dumps({'quad':Q,'thr':t}))
