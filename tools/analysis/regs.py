import sys, collections
d=open(sys.argv[1],'rb').read()[16:]
c=collections.Counter()
for i in range(len(d)-2):
    if d[i] in (0x8D,0x8E,0x8C,0xAD):   # STA/STX/STY/LDA abs
        a=d[i+1]|d[i+2]<<8
        if 0x5000<=a<0x5C00 or a in (0x8000,0x8001,0xA000,0xA001,0xC000,0xC001,0xE000,0xE001) or 0x6000<=a<0x6010:
            c[(('LDA' if d[i]==0xAD else 'ST*'),a)]+=1
names={0x5000:'sq1',0x5004:'sq2',0x5010:'pcm',0x5015:'snd_en',0x5100:'prgmode',0x5101:'chrmode',0x5104:'exram_mode',0x5105:'nt_map',0x5106:'fill',0x5113:'wram_bank',0x5114:'prg8',0x5115:'prgA',0x5116:'prgC',0x5203:'irq_line',0x5204:'irq_stat',0x5205:'mul_lo',0x5206:'mul_hi',0x8000:'mmc3sel',0x8001:'mmc3data',0xC000:'irqlatch',0xC001:'irqreload',0xE000:'irqoff',0xE001:'irqon',0xA000:'mirror',0xA001:'wram_prot'}
for (op,a),n in sorted(c.items(), key=lambda x:x[0][1]):
    if n>=2: print(f'{op} ${a:04X} {names.get(a,""):10s} x{n}')
