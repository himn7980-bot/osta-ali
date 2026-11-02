import json, math
S=20; M=20
def circ3(a,m,b):
    ax,ay=a;bx,by=m;cx,cy=b
    d=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    if abs(d)<1e-9: return None
    a2=ax*ax+ay*ay;b2=bx*bx+by*by;c2=cx*cx+cy*cy
    ux=(a2*(by-cy)+b2*(cy-ay)+c2*(ay-by))/d;uy=(a2*(cx-bx)+b2*(ax-cx)+c2*(bx-ax))/d
    return ux,uy,math.hypot(ax-ux,ay-uy)
def arcpts(a,m,b):
    c=circ3(a,m,b)
    if not c: return [a,b]
    nm=lambda v:(v%(2*math.pi)+2*math.pi)%(2*math.pi)
    ta=math.atan2(a[1]-c[1],a[0]-c[0]);d1=nm(math.atan2(m[1]-c[1],m[0]-c[0])-ta);d2=nm(math.atan2(b[1]-c[1],b[0]-c[0])-ta)
    sw=d2 if d1<d2 else d2-2*math.pi;k=max(4,math.ceil(abs(sw)/(math.pi/40)))
    return [(c[0]+c[2]*math.cos(ta+sw*i/k),c[1]+c[2]*math.sin(ta+sw*i/k)) for i in range(k+1)]
def build(name,typ,ops,room,ptype='ceil'):
    # ops: list of ('P',(u,v)) start, then ('L',(u,v)) or ('A',(u,v),bulge); closes to start
    pts=[ops[0][1]];segs=[]
    cur=ops[0][1]
    for o in ops[1:]+[('L',ops[0][1])]:
        p=o[1]
        if o[0]=='L':
            if math.hypot(p[0]-cur[0],p[1]-cur[1])<1e-6: continue
            segs.append(('L',cur,p))
        else:
            dx,dy=p[0]-cur[0],p[1]-cur[1];L=math.hypot(dx,dy);n=(-dy/L,dx/L)
            if n[0]*room[0]+n[1]*room[1]<0: n=(-n[0],-n[1])
            if o[2]<0: n=(-n[0],-n[1])
            sag=abs(o[2])*L;m=((cur[0]+p[0])/2+n[0]*sag,(cur[1]+p[1])/2+n[1]*sag)
            segs.append(('A',cur,p,m))
        cur=p
    poly=[]
    for s in segs:
        if s[0]=='L': poly.append(s[1])
        else: poly+=arcpts(s[1],s[3],s[2])[:-1]
    us=[p[0] for p in poly];vs=[p[1] for p in poly];u0,u1,v0,v1=min(us),max(us),min(vs),max(vs)
    W,H=u1-u0,v1-v0
    X=lambda p:{'x':round((p[0]-u0)*S+M,1),'y':round((v1-p[1])*S+M,1)}
    V=[];E=[]
    for s in segs:
        a=len(V);V.append(X(s[1]))
        if s[0]=='L': E.append({'t':'L','a':a})
        else:
            mm=X(s[3]);mm['mid']=1;V.append(mm);E.append({'t':'A','a':a,'m':a+1})
    for i,e in enumerate(E): e['b']=E[(i+1)%len(E)]['a']
    return {'name':name,'type':typ,'w':round(W,1),'h':round(H,1),'hcm':round(H,2),'ptype':ptype,
            'WW':round(W*S+2*M),'WH':round(H*S+2*M),'shape':{'V':V,'E':E},
            'pts':[[round(p[0]-u0,2),round(p[1]-v0,2)] for p in poly]}
fa=lambda n:str(n).translate(str.maketrans('0123456789.','۰۱۲۳۴۵۶۷۸۹٫'))
items=[]
CR=(1,-1)  # cornice room dir
def add(n,t,ops,room,pt='ceil'):items.append(build(n,t,ops,room,pt))
# --- گلویی
for h in [6,8,10,12,15,20]:
    w=round(h*.9,1)
    add(f'گلویی ساده {fa(h)} سانت','گلویی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.9)),('L',(w*.88,h*.9)),('A',(w*.12,h*.1),-.22),('L',(w*.12,0))],CR)
    add(f'گلویی مهره‌دار {fa(h)} سانت','گلویی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.9)),('L',(w*.9,h*.9)),('A',(w*.32,h*.3),-.2),('L',(w*.32,h*.26)),('A',(w*.32,h*.08),.5),('L',(w*.14,h*.08)),('L',(w*.14,0))],CR)
# --- قرنیز سقفی
for h in [10,12,15,20,25]:
    w=round(h*.85,1)
    add(f'قرنیز اُجی (S) {fa(h)} سانت','قرنیز سقفی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.9)),('L',(w*.92,h*.9)),('A',(w*.55,h*.5),-.18),('A',(w*.18,h*.1),.18),('L',(w*.18,0))],CR)
    add(f'قرنیز اُجی معکوس {fa(h)} سانت','قرنیز سقفی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.9)),('L',(w*.92,h*.9)),('A',(w*.55,h*.5),.18),('A',(w*.18,h*.1),-.18),('L',(w*.18,0))],CR)
    add(f'قرنیز پله‌دار {fa(h)} سانت','قرنیز سقفی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.86)),('L',(w*.86,h*.86)),('L',(w*.86,h*.78)),('A',(w*.86,h*.6),-.5),('L',(w*.86,h*.54)),('L',(w*.7,h*.54)),('L',(w*.7,h*.46)),('A',(w*.34,h*.14),-.2),('L',(w*.34,h*.08)),('L',(w*.2,h*.08)),('L',(w*.2,0))],CR)
    add(f'قرنیز دندانه‌ای {fa(h)} سانت','قرنیز سقفی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.8)),('L',(w*.8,h*.8)),('L',(w*.8,h*.6)),('L',(w*.6,h*.6)),('L',(w*.6,h*.4)),('L',(w*.42,h*.4)),('L',(w*.42,h*.2)),('L',(w*.25,h*.2)),('L',(w*.25,0))],CR)
    add(f'قرنیز کلاسیک مهره و گلویی {fa(h)} سانت','قرنیز سقفی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.88)),('A',(w,h*.72),.5),('L',(w*.88,h*.72)),('A',(w*.4,h*.3),-.2),('L',(w*.4,h*.24)),('L',(w*.3,h*.24)),('A',(w*.3,h*.06),.5),('L',(w*.15,h*.06)),('L',(w*.15,0))],CR)
# --- قرنیز کف
FR=(1,1)
for h in [8,10,12,15]:
    for t in [1.5,2]:
        add(f'قرنیز کف پخ‌دار {fa(h)}×{fa(t)}','قرنیز کف',[('P',(0,0)),('L',(t,0)),('L',(t,h-.8)),('L',(t*.45,h)),('L',(0,h))],FR,'floor')
        add(f'قرنیز کف اُجی {fa(h)}×{fa(t)}','قرنیز کف',[('P',(0,0)),('L',(t,0)),('L',(t,h*.78)),('A',(t*.55,h*.89),-.2),('A',(t*.15,h),.2),('L',(0,h))],FR,'floor')
    t=2
    add(f'قرنیز کف سرگرد {fa(h)}×{fa(t)}','قرنیز کف',[('P',(0,0)),('L',(t,0)),('L',(t,h-t/2)),('A',(0,h-t/2),.5)],FR,'floor')
    add(f'قرنیز کف پله‌دار {fa(h)}×{fa(t)}','قرنیز کف',[('P',(0,0)),('L',(t,0)),('L',(t,h*.82)),('L',(t*.55,h*.82)),('L',(t*.55,h)),('L',(0,h))],FR,'floor')
# --- قاب (in-plane width w, projection up)
PR=(0,1)
for w in [2,3,4,5,6]:
    add(f'قاب نیم‌گرد {fa(w)} سانت','قاب',[('P',(0,0)),('L',(w,0)),('A',(0,0),.5)],PR)
    add(f'قاب ربع‌گرد {fa(w)} سانت','قاب',[('P',(0,0)),('L',(w,0)),('A',(0,w*.6),.207)],PR)
    p=round(w*.5,2)
    add(f'قاب اُجی {fa(w)} سانت','قاب',[('P',(0,0)),('L',(w,0)),('L',(w,p*.3)),('A',(w*.5,p*.65),-.2),('A',(w*.1,p),.2),('L',(0,p))],PR)
    add(f'قاب پخ‌دار {fa(w)} سانت','قاب',[('P',(0,0)),('L',(w,0)),('L',(w,p*.4)),('L',(w*.75,p)),('L',(w*.25,p)),('L',(0,p*.4))],PR)
    add(f'قاب پله‌ای مهره‌دار {fa(w)} سانت','قاب',[('P',(0,0)),('L',(w,0)),('L',(w,p*.5)),('L',(w*.7,p*.5)),('A',(w*.2,p*.5),.5),('L',(0,p*.5))],PR)
# --- کمربندی
WR=(1,0)
for h in [5,6,8,10]:
    w=round(h*.35,1)
    add(f'کمربندی ساده {fa(h)} سانت','کمربندی / ابزار دیواری',[('P',(0,0)),('L',(w*.4,0)),('A',(w,h*.35),.2),('L',(w,h*.65)),('A',(w*.4,h),.2),('L',(0,h))],WR)
    add(f'کمربندی مهره‌دار {fa(h)} سانت','کمربندی / ابزار دیواری',[('P',(0,0)),('L',(w*.6,0)),('L',(w*.6,h*.3)),('A',(w*.6,h*.7),.5),('L',(w*.6,h)),('L',(0,h))],WR)
# --- چهارچوب
for w in [6,8,10,12]:
    p=round(w*.25,1)
    add(f'چهارچوب در و پنجره کلاسیک {fa(w)} سانت','چهارچوب در و پنجره',[('P',(0,0)),('L',(w,0)),('L',(w,p)),('L',(w*.8,p)),('A',(w*.6,p*.6),-.2),('L',(w*.3,p*.6)),('L',(w*.3,p*.45)),('L',(0,p*.4))],PR)
    add(f'چهارچوب پله‌ای {fa(w)} سانت','چهارچوب در و پنجره',[('P',(0,0)),('L',(w,0)),('L',(w,p)),('L',(w*.65,p)),('L',(w*.65,p*.7)),('L',(w*.3,p*.7)),('L',(w*.3,p*.45)),('L',(0,p*.45))],PR)
# --- فیتیله / نور مخفی
for h in [10,12,15,20]:
    w=round(h*1.0,1)
    add(f'فیتیله نور مخفی {fa(h)} سانت','فیتیله / نور مخفی',[('P',(0,0)),('L',(0,h*.45)),('L',(w*.78,h*.45)),('L',(w*.78,h)),('L',(w,h)),('L',(w,h*.5)),('A',(w*.32,h*.08),-.2),('L',(w*.2,h*.08)),('L',(w*.2,0))],CR)
# --- نوار سقفی
for h in [4,6,8,10]:
    for w in [2,3]:
        add(f'نوار سقفی {fa(h)}×{fa(w)}','نوار سقفی',[('P',(0,0)),('L',(0,h)),('L',(w,h)),('L',(w,h*.25)),('L',(w*.6,0))],CR)
for i,it in enumerate(items): it['id']='c%d'%(i+1)
json.dump(items,open('/home/claude/gach/catalog.json','w'),ensure_ascii=False,separators=(',',':'))
from collections import Counter;print(len(items),Counter(i['type'] for i in items))
