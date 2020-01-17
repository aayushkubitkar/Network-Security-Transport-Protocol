import socket
import hashlib
from struct import *
def handleClientHello(clientsocket, recv_buff):
    print ("inside clienthello")
    if recv_buff:
        version = unpack('>2B', recv_buff[1:3])
        length = unpack('>H', recv_buff[3:5])
        if version[0]!=1:
            print("client not supported with version", version[0])
            errorResponse(clientsocket, "Client version not compliant")
            return False
        #userAgentString = recv_buff[5:length[0]+5].decode("utf-8")
        #print (payload)
        serverHello(clientsocket)
        return True
def serverHello(clientsocket):
    print ("inside server hello")
    minor_v = 1
    userAgentString="Hi Client"
    res = pack('>BBBH', 1, 1, minor_v, len(userAgentString))+bytes(userAgentString, "utf-8")
    clientsocket.send(res)

def handlePingReq(clientsocket, recv_buff):
    print ("inside ping req")
    print("inside handlePingReq", recv_buff)
    length = unpack('>H', recv_buff[1:3])
    data = recv_buff[3:length[0]+3]
    print (data)
    hash_alg = unpack('>B', recv_buff[length[0]+3:length[0]+4])
    print (hash_alg[0])
    return pingResponse(clientsocket, data, hash_alg[0])
def pingResponse(clientsocket,data,hash_alg):
    print("inside pingResponse")

    if hash_alg==0:
        res = pack('>BH', 4, len(data))+bytes(data)
        clientsocket.send(res)
        return True
    elif hash_alg==1:
        hashVal= hashlib.sha256(data)
    elif hash_alg==2:
        hashVal= hashlib.sha512(data)
    else:
        errorResponse(clientsocket, "Invalid hash algorithm")
        return False
    hash_data=hashVal.digest()
    res = pack('>BH', 4, len(hash_data))+bytes(hash_data)
    clientsocket.send(res)
    return True

def handleStoreReq(clientsocket, recv_buff):
    print ("inside handleStoreReq")
    lengthOfKey=unpack('>H',recv_buff[1:3])
    key=recv_buff[3:lengthOfKey[0]+3].decode("utf-8")
    lengthOfValue=unpack('>H',recv_buff[lengthOfKey[0]+3:lengthOfKey[0]+5])
    value=recv_buff[lengthOfKey[0]+5:lengthOfKey[0]+5+lengthOfValue[0]]
    valueStore[key]=value
    storeResponse(clientsocket,value)
    return True
def storeResponse(clientsocket, value):
    print ("inside storeResponse")
    hashVal= hashlib.sha256(value)
    hash_data = hashVal.digest()
    res = pack('>BH', 8, len(hash_data)) + hash_data + pack('B', 1)
    clientsocket.send(res)

def handleLoadReq(clientsocket, recv_buff):
    print("inside handleLoadReq")
    lengthOfKey=unpack('>H',recv_buff[1:3])
    key = recv_buff[3:lengthOfKey[0] + 3].decode("utf-8")
    if key:
        loadResponse(clientsocket, key)
        return True
    else:
        errorResponse(clientsocket, "Key is null")
        return False
def loadResponse(clientsocket, key):
    print("inside loadResponse")
    print (key)
    if key in valueStore:
        value=valueStore[key]
    else:
        value=[]
    print (value, len(value))
    res = pack('>BH', 6, len(value))+bytes(value)
    clientsocket.send(res)
def errorResponse(clientsocket, msg):
    res = pack('>BH', 2, len(msg))+ bytes(msg, "utf-8")
    clientsocket.send(res)
    return False

RECV_BUFFER_SIZE = 1024
HOST = '0.0.0.0'
PORT = 22300
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
valueStore={}
response=None
new_msg = True
while True:
    print("waiting for connection...")
    clientsocket, addr = s.accept()
    print("new connection received")
    while True:
        print("connected by", addr)
        recv_buff = bytearray(RECV_BUFFER_SIZE)
        numberOfBytes = clientsocket.recv_into(recv_buff)
        if numberOfBytes!=0:
            tag = unpack('>B', recv_buff[:1])
            if new_msg and tag[0] != 0:
                response = errorResponse(clientsocket, "Client Not Initialized")
            else:
                new_msg = False
                switcher = {
                    0: handleClientHello,
                    3: handlePingReq,
                    5: handleLoadReq,
                    7: handleStoreReq
                }
                print(tag[0])
                func = switcher.get(tag[0])
                response = func(clientsocket, recv_buff)
                print(response)
            if not response:
                # clientsocket.close()
                break
        else:
            break





