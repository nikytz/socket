import socket
import json

HOST = '127.0.0.1'
PORT = 65432
DIM_BUFFER = 1024

# Usiamo 'with' per gestire il socket del client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
    sock_service.connect((HOST, PORT))
    
    # Input dell'utente
    n1 = float(input("Inserisci il primo numero: "))
    op = input("Inserisci l'operazione (+, -, *, /): ")
    n2 = float(input("Inserisci il secondo numero: "))
    
    # Creazione del pacchetto JSON
    messaggio_dict = {
        "primoNumero": n1,
        "operazione": op,
        "secondoNumero": n2
    }
    messaggio_json = json.dumps(messaggio_dict)
    
    # Invio dati
    sock_service.sendall(messaggio_json.encode("UTF-8"))
    
    # Ricezione risultato
    data = sock_service.recv(DIM_BUFFER)
    print(f"Risultato ricevuto dal server: {data.decode('UTF-8')}")

# Qui il socket è già stato chiuso automaticamente grazie a 'with'