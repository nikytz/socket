
import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 1024
NUM_MESSAGES = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(NUM_MESSAGES):
    print(f"\n--- Calcolo {i+1} di {NUM_MESSAGES} ---")
    primoNumero = float(input("Inserisci il primo numero: "))
    operazione = input("Inserisci l'operazione (+, -, *, /): ")
    secondoNumero = float(input("Inserisci il secondo numero: "))

    messaggio_dict = {
        "primoNumero": primoNumero,
        "operazione": operazione,
        "secondoNumero": secondoNumero
    }

    # Trasforma in JSON e invia
    messaggio_json = json.dumps(messaggio_dict)
    sock.sendto(messaggio_json.encode("UTF-8"), (SERVER_IP, SERVER_PORT)) # Usato 'sock'

    # Ricezione del risultato dal server
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"Risultato dal server: {data.decode()}")

sock.close()




