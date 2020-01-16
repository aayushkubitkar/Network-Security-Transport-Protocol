import socket
import hashlib
import binascii
from struct import *
def handleClientHello(clientsocket, recv_buff):
    if recv_buff:
        version = unpack('>2B', recv_buff[1:3])
        length = unpack('>H', recv_buff[3:5])
        msg_end = length[0]+5
        if version[0]!=1:
            print("client not supported with version", version[0])
            return
        payload = recv_buff[5:msg_end].decode("utf-8")
        print (payload)
        serverHello(clientsocket)
def serverHello(clientsocket):
    msg_tag = 2
    major_v = 1
    minor_v = 1
    user_agent_string="Hi Client"
    server_hello = pack('>hhhh', msg_tag, major_v, minor_v, len(user_agent_string))+bytes(user_agent_string,"utf-8")
    clientsocket.send(server_hello)

def handlePingReq(clientsocket, recv_buff):
    print("inside handlePingReq", recv_buff)
    length = unpack('>H', recv_buff[1:3])
    data = recv_buff[3:length[0]+3]
    print (data)
    hash_alg = unpack('>B', recv_buff[length[0]+3:length[0]+4])
    print (hash_alg[0])
    pingResponse(clientsocket, data, hash_alg[0])
def pingResponse(clientsocket,data,hash_alg):
    print("inside pingResponse")

    if hash_alg==0:
        res = pack('>BH', 4, len(bytes(data)))+bytes(data,"utf-8")
        clientsocket.send(res)
        return
    elif hash_alg==1:
        hashVal= hashlib.sha256(data)
    elif hash_alg==2:
        hashVal= hashlib.sha512(data)
    else:
        print ("wrong algorithm code passed")
        return
    hex_data=hashVal.hexdigest()
    res = pack('>BH', 4, len(hex_data))+bytes(hex_data,"utf-8")
    clientsocket.send(res)

def handleStoreReq(clientsocket, recv_buff):
    print ("inside handleStoreReq")
    lengthOfKey=unpack('>H',recv_buff[1:3])
    key=recv_buff[3:lengthOfKey[0]+3].decode("utf-8")
    lengthOfValue=unpack('>H',recv_buff[lengthOfKey[0]+3:lengthOfKey[0]+5])
    value=recv_buff[lengthOfKey[0]+5:lengthOfKey[0]+5+lengthOfValue[0]]
    valueStore[key]=value
    storeResponse(clientsocket,value)
def storeResponse(clientsocket, value):
    print ("inside storeResponse")
    hashVal= hashlib.sha256(value)
    hex_data = hashVal.hexdigest()
    # print (hex_data)
    res = pack('>BH', 8, len(hex_data)) + bytes(hex_data, "utf-8") + pack('B',1)
    clientsocket.send(res)

def handleLoadReq(clientsocket, recv_buff):
    print("inside handleLoadReq")
    lengthOfKey=unpack('>H',recv_buff[1:3])
    key = recv_buff[3:lengthOfKey[0] + 3].decode("utf-8")
    if key:
        loadResponse(clientsocket, key)
def loadResponse(clientsocket, key):
    print("inside loadResponse")
    print (key)
    if key in valueStore:
        value=valueStore[key]
    else:
        value=[1]
    print (value, len(value))
    res = pack('>BH', 6, len(value))+bytes(value)
    clientsocket.send(res)
HOST = 'localhost'
PORT = 1234
HEADERSIZE = 5
RECV_BUFFER_SIZE = 100
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
valueStore={}
while True:
    print("waiting for connection...")
    clientsocket, addr = s.accept()
    print("new connection received")
    with clientsocket:
        print("connected by", addr)
        new_msg = True
        payload=''
        while True:
            recv_buff= bytearray(1024)
            numberOfBytes = clientsocket.recv_into(recv_buff)
            if not numberOfBytes:break
            if new_msg:
                tag = unpack('>B', recv_buff[:1])
                switcher = {
                    0: handleClientHello,
                    3: handlePingReq,
                    5: handleLoadReq,
                    7: handleStoreReq
                }
                func = switcher.get(tag[0])
                func(clientsocket, recv_buff)
                break



