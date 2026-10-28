import sys
def banks(path, sz=0x2000):
    d=open(path,'rb').read()[16:]; return [d[i:i+sz] for i in range(0,len(d),sz)]
def free(b):
    # longest/total runs of FF or 00 >= 16 bytes
    tot=0; i=0
    while i<len(b):
        j=i
        while j<len(b) and b[j]==b[i] and b[i] in (0,0xff): j+=1
        if j-i>=16: tot+=j-i
        i=max(j,i+1)
    return tot
mode=sys.argv[1]
if mode=='free':
    bs=banks(sys.argv[2]); t=0
    for n,b in enumerate(bs):
        f=free(b); t+=f
        print(f'{n:02X}:{f*100//len(b):3d}%', end='  ' if (n+1)%8 else '\n')
    print('total free-ish bytes', t, f'({t/1024:.1f} KB)')
elif mode=='diff':
    a=banks(sys.argv[2]); b=banks(sys.argv[3]); same=0
    for n,bb in enumerate(b):
        # find best-matching original bank (hack may relocate)
        best=max(range(len(a)), key=lambda k: sum(x==y for x,y in zip(a[k],bb)))
        pct=sum(x==y for x,y in zip(a[best],bb))*100//len(bb)
        print(f'{n:02X}<-{best:02X}:{pct:3d}%', end='  ' if (n+1)%8 else '\n')
