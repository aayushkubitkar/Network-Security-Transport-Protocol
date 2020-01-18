import socket
import select
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
            return
        serverHello(clientsocket)

def serverHello(clientsocket):
    print ("inside server hello")
    minor_v = 1
    userAgentString="Hi Client"
    res = pack('>BBBH', 1, 1, minor_v, len(userAgentString))+bytes(userAgentString, "utf-8")
    responseMessage[clientsocket] = res

def handlePingReq(clientsocket, recv_buff):
    print ("inside ping req")
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
        res = pack('>BH', 4, len(data))+bytes(data)
        responseMessage[clientsocket] = res
        return
    elif hash_alg==1:
        hashVal= hashlib.sha256(data)
    elif hash_alg==2:
        hashVal= hashlib.sha512(data)
    else:
        errorResponse(clientsocket, "Invalid hash algorithm")
        return
    hash_data=hashVal.digest()
    res = pack('>BH', 4, len(hash_data))+bytes(hash_data)
    responseMessage[clientsocket] = res

def handleStoreReq(clientsocket, recv_buff):
    print ("inside handleStoreReq")
    lengthOfKey=unpack('>H',recv_buff[1:3])
    key=recv_buff[3:lengthOfKey[0]+3].decode("utf-8")
    lengthOfValue=unpack('>H',recv_buff[lengthOfKey[0]+3:lengthOfKey[0]+5])
    value=recv_buff[lengthOfKey[0]+5:lengthOfKey[0]+5+lengthOfValue[0]]
    valueStore[clientsocket]={key:value}
    storeResponse(clientsocket,key)

def storeResponse(clientsocket, key):
    print ("inside storeResponse")
    hashVal= hashlib.sha256(valueStore[clientsocket][key])
    hash_data = hashVal.digest()
    res = pack('>BH', 8, len(hash_data)) + hash_data + pack('B', 1)
    responseMessage[clientsocket] = res

def handleLoadReq(clientsocket, recv_buff):
    print("inside handleLoadReq")
    lengthOfKey=unpack('>H',recv_buff[1:3])
    key = recv_buff[3:lengthOfKey[0] + 3].decode("utf-8")
    if key:
        loadResponse(clientsocket, key)
    else:
        errorResponse(clientsocket, "Key is null")
        return False

def loadResponse(clientsocket, key):
    print("inside loadResponse")
    print (key)
    try:
        value=valueStore[clientsocket][key]
    except KeyError:
        value=[]
    print (value, len(value))
    res = pack('>BH', 6, len(value))+bytes(value)
    responseMessage[clientsocket] = res

def errorResponse(clientsocket, msg):
    res = pack('>BH', 2, len(msg))+ bytes(msg, "utf-8")
    responseMessage[clientsocket] = res
    incoming.remove(clientsocket)

RECV_BUFFER_SIZE = 1024
HOST = '0.0.0.0'
PORT = 22300
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

incoming=[server]
outgoing=[]
responseMessage={}
clientInit={}
valueStore={}

while incoming:
    print("start waiting")
    reads, writes, exceptions = select.select(incoming, outgoing, incoming)
    for s in reads:
        if s is server:
            print("connection accepted from", s)
            clientsocket, addr = server.accept()
            clientsocket.setblocking(False)
            incoming.append(clientsocket)
        else:
            print("data read from socket", s)
            recv_buff = bytearray(RECV_BUFFER_SIZE)
            numberOfBytes = s.recv_into(recv_buff)
            if numberOfBytes != 0:
                outgoing.append(s)
                tag = unpack('>B', recv_buff[:1])
                if  tag[0] != 0:
                    try:
                        if clientInit[s]:
                            switcher = {
                                3: handlePingReq,
                                5: handleLoadReq,
                                7: handleStoreReq
                            }
                            print(tag[0])
                            func = switcher.get(tag[0])
                            func(s, recv_buff)
                    except KeyError:
                        print (tag[0])
                        errorResponse(s, "Client Not Initialized")
                elif tag[0]==0:
                    handleClientHello(s, recv_buff)
                    clientInit[s] = True
            else:
                print ("received no data")
                incoming.remove(s)
                s.close()
                if s in responseMessage:
                    del responseMessage[s]
                if s in clientInit:
                    del clientInit[s]
                if s in valueStore:
                    del valueStore[s]
    for s in writes:
        try:
            print ("writing data to socket",s, responseMessage[s])
            s.send(responseMessage[s])
            outgoing.remove(s)
        except:
            outgoing.remove(s)
    for s in exceptions:
        print ("inside exceptions")
        if s in outgoing:
            outgoing.remove(s)
        incoming.remove(s)
        s.close()
        if s in responseMessage:
            del responseMessage[s]
        if s in clientInit:
            del clientInit[s]
        if s in valueStore:
            del valueStore[s]
