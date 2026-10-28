import sys
sys.path.insert(0, sys.argv[1])
from py65.devices.mpu6502 import MPU
from py65.disassembler import Disassembler
rom=open(sys.argv[2],'rb').read()[16:]
bank=int(sys.argv[3],16); cpubase=int(sys.argv[4],16)
mpu=MPU(); mem=mpu.memory
blk=rom[bank*0x2000:(bank+1)*0x2000]; mem[cpubase:cpubase+0x2000]=list(blk)
# also map fixed $E000 bank (last)
last=rom[-0x2000:]; mem[0xE000:0x10000]=list(last)
if cpubase!=0xC000: mem[0xC000:0xE000]=list(rom[-0x4000:-0x2000])
d=Disassembler(mpu)
if sys.argv[5]=='vec':
    for v,n in ((0xFFFA,'NMI'),(0xFFFC,'RESET'),(0xFFFE,'IRQ')): print(n, hex(mem[v]|mem[v+1]<<8))
else:
    pc=int(sys.argv[5],16); n=int(sys.argv[6])
    for _ in range(n):
        l,t=d.instruction_at(pc); print(f'{pc:04X}  {t}'); pc+=l
