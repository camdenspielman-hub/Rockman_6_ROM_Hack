import sys,re
d=open(sys.argv[1],'rb').read(); a=int(sys.argv[2],16); n=int(sys.argv[3],16); base=int(sys.argv[4])  # base: byte value of 'A'
s=''.join(chr(b-base+65) if base<=b<base+26 else ('.' if True else '') for b in d[a:a+n])
# collapse to words
print(re.sub(r'\.{2,}',' | ',s))
