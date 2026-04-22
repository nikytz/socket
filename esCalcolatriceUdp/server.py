# Ricevo i dati
import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("Server in attesa di dati per il calcolo...")

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE) # Usato 'sock' invece di 's'
    if not data:
        break
    
    # Decodifica e trasforma in dizionario
    stringa_ricevuta = data.decode()
    dizionario = json.loads(stringa_ricevuta)
    
    n1 = dizionario["primoNumero"]
    op = dizionario["operazione"]
    n2 = dizionario["secondoNumero"]
    
    print(f"Ricevuto da {addr}: {n1} {op} {n2}")

    # Logica del calcolo
    if op == "+":
        risultato = n1 + n2
    elif op == "-":
        risultato = n1 - n2
    elif op == "*":
        risultato = n1 * n2
    elif op == "/":
        risultato = n1 / n2 if n2 != 0 else "Errore: Div per 0"
    else:
        risultato = "Operazione non valida"

    # Invio del risultato reale invece di "pong"
    sock.sendto(str(risultato).encode(), addr)


