from socket import *
serverPort = 12000                                              #ezen a porton fog hallgatni a szerver
serverSocket = socket(AF_INET,SOCK_STREAM)                      #letrehozunk egy uj TCP portot(SOCK_STREAM)
                                                                #UDP eseten ez SOCK_DGRAM lenne
                                                                #az AF_INET meghatarozza, hogy IPv4-et hasznaljunk
                                                                #ami [0-255].[0-255].[0-255].[0-255] alakú
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)            #megengedi, hogy a portot ujrahasznaljuk, ezzel megelozve a "Address already in use" hibat
serverSocket.bind(('localhost',serverPort))                     #letrehozza a szoketet, ami csak helyi kapcsolatokat fog fogadni
                                                                #ezeket az 12000-es porton fogja hallgatni
serverSocket.listen(5)                                          #megadja, hogy egyszerre csak 1 kliensre hallgasson
print ('The server is ready to receive')
while True:                                                     #addig varja a jeleket, ameddig mi kezzel le nem allitjuk(vagy exit kulcsoszoval a klienstol)
    connectionSocket, addr = serverSocket.accept()              #egy uj szoketet hoz letre a klienssel valo kapcsolodashoz, az addr a kliens cime(IP, Port)
    request = connectionSocket.recv(1024).decode()             #lekerjuk a kuldott uzenetet es dekodoljuk
    
    request_lines = request.split('\r\n')
    for line in request_lines:
        if line:
            print(line)
    #print(f"Received request: {request_line}")
    
    response_body = "<html><body><h1>Hello from my server!</h1></body></html>"
    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\nContent-Type: text/html\r\n\r\n{response_body}"

    connectionSocket.send(response.encode())         #es visszakuldjuk a kliensnek
    connectionSocket.close()     