#Ferencz Peter, 522/1

from socket import *
serverPort = 12000                                              #ezen a porton fog hallgatni a szerver
serverSocket = socket(AF_INET,SOCK_STREAM)                      #letrehozunk egy uj TCP portot(SOCK_STREAM)
                                                                #UDP eseten ez SOCK_DGRAM lenne
                                                                #az AF_INET meghatarozza, hogy IPv4-et hasznaljunk
                                                                #ami [0-255].[0-255].[0-255].[0-255] alakú
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)            #megengedi, hogy a portot ujrahasznaljuk, ezzel megelozve a "Address already in use" hibat
serverSocket.bind(('localhost',serverPort))                     #letrehozza a szoketet, ami csak helyi kapcsolatokat fog fogadni
                                                                #ezeket az 12000-es porton fogja hallgatni
serverSocket.listen(1)                                          #megadja, hogy egyszerre csak 1 kliensre hallgasson
print ('The server is ready to receive')
while True:                                                     #addig varja a jeleket, ameddig mi kezzel le nem allitjuk(vagy exit kulcsoszoval a klienstol)
    connectionSocket, addr = serverSocket.accept()              #egy uj szoketet hoz letre a klienssel valo kapcsolodashoz, az addr a kliens cime(IP, Port)
    sentence = connectionSocket.recv(1024).decode()             #lekerjuk a kuldott uzenetet es dekodoljuk
    if sentence == "exit":                                      #ha az uzenet exit volt, akkor kilepunk
        connectionSocket.send("I stopped".encode())
        exit()
    capitalizedSentence = sentence.upper()                      #nagybetusse alakitjuk
    connectionSocket.send(capitalizedSentence.encode())         #es visszakuldjuk a kliensnek
    connectionSocket.close()                                    #bezarjuk az adott socketet