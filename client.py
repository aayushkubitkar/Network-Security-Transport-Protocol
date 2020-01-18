import socket
from struct import *
HOST = 'localhost'
PORT = 22300
HEADERSIZE=5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#Client Hello
msg_tag = 0
major_v = 0
minor_v = 1
user_agent_string="Hi server"
client_hello = pack('>3BH', msg_tag, major_v, minor_v, len(user_agent_string))+bytes(user_agent_string,"utf-8")
s.send(client_hello)
recv_buff = bytearray(1024)
nbytes= s.recv_into(recv_buff)
length_of_msg= unpack('>H',recv_buff[3:5])
print (recv_buff[3:length_of_msg[0]+5])

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((HOST, PORT))
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3.connect((HOST, PORT))
s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s4.connect((HOST, PORT))
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT))
msg_tag = 0
major_v = 1
minor_v = 1
user_agent_string="Hi server"
client_hello = pack('>3BH', msg_tag, major_v, minor_v, len(user_agent_string))+bytes(user_agent_string,"utf-8")
s1.send(client_hello)
data =s1.recv(1024)
print (data)

store_tag=7
key="a"
value=[1,2,4]
store_req = pack('>BH', store_tag, len(key.encode()))+bytes(key,"utf-8")+pack('>H',len(value))+bytes(value)
s1.send(store_req)
data =s1.recv(1024)
print (data)

load_tag=5
key="a"
load_req = pack('>BH',load_tag, len(key.encode()))+bytes(key,"utf-8")
s1.send(load_req)
# recv_buffer = bytearray(1024)
# nbytes= s.recv_into(recv_buffer)
# length_of_value=unpack('>H',recv_buffer[1:3])
# print (recv_buffer)
# print ("received: ", recv_buffer[3:length_of_value[0]+3])
data =s1.recv(1024)
print (data)
#Ping Request
# ping_tag = 3
# a=[1,2,4]
# hash_alg=0
# ping_req = pack('>BH',ping_tag,len(a))+bytes(a)+pack('>B',hash_alg)
# s1.send(ping_req)
# recv_buff1 = bytearray(1024)
# n1bytes= s1.recv_into(recv_buff1)
# length_of_msg1= unpack('>H',recv_buff1[1:3])
# print (length_of_msg1[0])
# print("received: ", recv_buff1[3:length_of_msg1[0]+3])

# Store Request
store_tag=7
key="a"
value=[1,2,3]
store_req = pack('>BH', store_tag, len(key.encode()))+bytes(key,"utf-8")+pack('>H',len(value))+bytes(value)
s.send(store_req)
data =s.recv(1024)
print (data)
# recv_buff = bytearray(1024)
# nobytes= s1.recv_into(recv_buff)
# print (recv_buff)
# length_of_hash=unpack('>H',recv_buff[1:3])
# print ("received: ", recv_buff[3:length_of_hash[0]+3])

#039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81
#039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81


#Load Request
load_tag=5
key="a"
load_req = pack('>BH',load_tag, len(key.encode()))+bytes(key,"utf-8")
s.send(load_req)
# recv_buffer = bytearray(1024)
# nbytes= s.recv_into(recv_buffer)
# length_of_value=unpack('>H',recv_buffer[1:3])
# print (recv_buffer)
# print ("received: ", recv_buffer[3:length_of_value[0]+3])
data =s.recv(1024)
print (data)