import socket
from struct import *
HOST = 'localhost'
PORT = 1234
HEADERSIZE=5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

#Client Hello
msg_tag = 0
major_v = 1
minor_v = 1
user_agent_string="Hi server"
client_hello = pack('>3BH', msg_tag, major_v, minor_v, len(user_agent_string))+bytes(user_agent_string,"utf-8")
#s.send(client_hello)

#Ping Request
# ping_tag = 3
# a=[1,2,3]
# hash_alg=1
# ping_req = pack('>BH',ping_tag,len(a))+bytes(a)+pack('>B',hash_alg)
# s.send(ping_req)
# recv_buff = bytearray(1024)
# bytes= s.recv_into(recv_buff)
# length_of_msg= unpack('>H',recv_buff[1:3])
# print (length_of_msg[0])
# print("received: ", recv_buff[3:length_of_msg[0]+3].decode())

# Store Request
# store_tag=7
# key="a"
# value=[1,2,3]
# store_req = pack('>BH', store_tag, len(key.encode()))+bytes(key,"utf-8")+pack('>H',len(value))+bytes(value)
# s.send(store_req)
# recv_buff = bytearray(1024)
# bytes= s.recv_into(recv_buff)
# length_of_hash=unpack('>H',recv_buff[1:3])
# print ("received: ", recv_buff[3:length_of_hash[0]+3].decode())

#039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81
#039058c6f2c0cb492c533b0a4d14ef77cc0f78abccced5287d84a1a2011cfb81


#Load Request
load_tag=5
key="a"
load_req = pack('>BH',load_tag, len(key.encode()))+bytes(key,"utf-8")
s.send(load_req)
recv_buff = bytearray(1024)
bytes= s.recv_into(recv_buff)
length_of_value=unpack('>H',recv_buff[1:3])
print ("received: ", recv_buff[3:length_of_value[0]+3])
