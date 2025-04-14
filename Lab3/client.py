from socket import *

def send_command(sock, message):
    print('C:', message.strip())
    sock.sendall(message.encode())

def receive_response(sock):
    response = sock.recv(1024).decode()
    print('S:', response.strip())
    if response.startswith(("4", "5")):
        print('An error ocurred!')
        sock.close()
        exit(1)
    return response

 
from_email_adress = input('Sender email adress: ')
to_email_adress = input('Receiver email adress: ')
subject = input('Emails subject: ')
body = input('Body: ')


serverName = 'localhost'
serverPort = 2525

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

 
receive_response(clientSocket)

 
send_command(clientSocket, "HELO localhost\r\n")
receive_response(clientSocket)

send_command(clientSocket, f"MAIL FROM: <{from_email_adress}>\r\n")
receive_response(clientSocket)

send_command(clientSocket, f"RCPT TO: <{from_email_adress}>\r\n")
receive_response(clientSocket)

send_command(clientSocket, "DATA\r\n")
receive_response(clientSocket)

email_lines = [
    f"From: {from_email_adress}",
    f"To: {to_email_adress}",
    f"Subject: {subject}",
    "",
    body,
    "."
]
email_message = "\r\n".join(email_lines) + "\r\n"

send_command(clientSocket, email_message)
receive_response(clientSocket)

 
send_command(clientSocket, "QUIT\r\n")
receive_response(clientSocket)

clientSocket.close()
print("Success")
