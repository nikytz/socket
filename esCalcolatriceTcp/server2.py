import socket
import json

IP = "127.0.0.1"
PORTA = 65432
DIM_BUFFER = 1024

# Usiamo 'with' per creare il socket del server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
    sock_server.bind((IP, PORTA))
    sock_server.listen()
    print(f"Server Calcolatrice TCP in ascolto su {IP}:{PORTA}...")

    while True:
        # Accetta la connessione dal client
        sock_service, address_client = sock_server.accept()
        
        # Usiamo 'with' anche per gestire la singola connessione del client
        with sock_service as sock_client:
            print(f"Connessione stabilita con {address_client}")
            
            # Ricezione dei dati
            data = sock_client.recv(DIM_BUFFER).decode("UTF-8")
            if not data:
                break
                
            dati_ricevuti = json.loads(data)
            n1 = dati_ricevuti["primoNumero"]
            op = dati_ricevuti["operazione"]
            n2 = dati_ricevuti["secondoNumero"]
            
            # Logica del calcolo
            if op == "+": risultato = n1 + n2
            elif op == "-": risultato = n1 - n2
            elif op == "*": risultato = n1 * n2
            elif op == "/": risultato = n1 / n2 if n2 != 0 else "Errore: Div per 0"
            else: risultato = "Operazione non valida"
            
            # Invio della risposta
            sock_client.sendall(str(risultato).encode("UTF-8"))