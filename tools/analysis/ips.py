import sys
def apply_ips(rom, patch):
    rom = bytearray(rom); assert patch[:5]==b'PATCH'; i=5; recs=[]
    while True:
        if patch[i:i+3]==b'EOF' and (i+3==len(patch) or len(patch)-i-3==3): 
            trunc = patch[i+3:]; break
        off=int.from_bytes(patch[i:i+3],'big'); sz=int.from_bytes(patch[i+3:i+5],'big'); i+=5
        if sz==0:
            rl=int.from_bytes(patch[i:i+2],'big'); val=patch[i+2:i+3]; i+=3; data=val*rl
        else:
            data=patch[i:i+sz]; i+=sz
        if off+len(data)>len(rom): rom.extend(b'\0'*(off+len(data)-len(rom)))
        rom[off:off+len(data)]=data; recs.append((off,len(data)))
    if trunc: rom=rom[:int.from_bytes(trunc,'big')]
    return rom, recs
if __name__=='__main__':
    rom=open(sys.argv[1],'rb').read(); p=open(sys.argv[2],'rb').read()
    out,recs=apply_ips(rom,p); open(sys.argv[3],'wb').write(out)
    print(len(out), len(recs), 'records; bytes written', sum(r[1] for r in recs))
