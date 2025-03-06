#Ferencz Peter, 522/1

from socket import *
serverName = 'localhost'                            #megadjuk, hogy milyen cimre kuldje az infokat
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)         #megadja, hogy milyen IP-t es, hogy TCP-t fogunk hasznalni
clientSocket.connect((serverName,serverPort))       #itt kapcsolodunk a szerverhez, letrejon a TCP kapcsolat
sentence = input('Input lowercase sentence:')       #bekerjuk a szoveget    
clientSocket.send(sentence.encode())                #elkuldjuk a servernek
modifiedSentence = clientSocket.recv(1024)          #varjuk az infot a szervertol
print ('From Server:', modifiedSentence.decode())
clientSocket.close()