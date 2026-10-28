import sys, collections
d=open(sys.argv[1],'rb').read()
words=sys.argv[2:]
for w in words:
    diffs=[ord(w[i+1])-ord(w[i]) for i in range(len(w)-1)]; hits=collections.Counter()
    for i in range(len(d)-len(w)):
        ok=True
        for k,df in enumerate(diffs):
            if d[i+k+1]-d[i+k]!=df: ok=False; break
        if ok: hits[d[i]-ord(w[0])]+=1; 
        if ok and hits[d[i]-ord(w[0])]<=3: print(w, hex(i), 'offset', d[i]-ord(w[0]))
    print(w, dict(hits))
