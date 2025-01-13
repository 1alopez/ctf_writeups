import sys
import socket
HOST = '34.66.235.106' 
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect ((HOST,PORT))

for i in range(0,1001):
    data = s.recv(1024).decode()
    print(data)

    res = data.splitlines()

    if i == 0:
        equation = res[3]
        #print(f"Equation is: {equation[10:]}")

        ans = eval(equation[10:])
        #print(f"Answer is: {ans}")
    else:
        equation = res[1]
        #print(f"Equation is: {equation[10:]}")

        ans = eval(equation[10:])
        #print(f"Answer is: {ans}")
    s.send(str(ans).encode() + b'\n')


    

