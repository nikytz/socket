# Client TCP multithread che invia NUM_WORKERS richieste contemporanee al server
# Ogni richiesta contiene un'operazione aritmetica da eseguire

import socket         # Per la comunicazione di rete
import json           # Per la codifica/decodifica JSON
import random         # Per generare numeri casuali
import time           # Per misurare i tempi di esecuzione
import threading      # Per gestire l'esecuzione parallela (multithreading)

# --- Configurazione ---
HOST = "127.0.0.1"           # IP del server
PORT = 65432                # Porta del server (modificata per combaciare con il server precedente)
NUM_WORKERS = 15            # Numero di richieste (thread) da inviare in parallelo
OPERAZIONI = ["+", "-", "*", "/", "%"]  # Lista delle operazioni consentite

# 1: Funzione che definisce il comportamento di ogni singolo thread "lavoratore"
def genera_richieste(address, port):
    # 2: Apertura del socket TCP utilizzando il costrutto 'with' per la chiusura automatica
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
        sock_service.connect((address, port))  # Connessione al server

        # 3: Generazione casuale dei numeri e scelta di un'operazione dalla lista
        primoNumero = random.randint(0, 100)
        operazione = OPERAZIONI[random.randint(0, 3)]  # Scegli operazione a caso (tra le prime 4)
        secondoNumero = random.randint(0, 100)

        # 4: Creazione del dizionario dati e conversione in stringa formato JSON
        messaggio = {
            "primoNumero": primoNumero,
            "operazione": operazione,
            "secondoNumero": secondoNumero
        }
        messaggio = json.dumps(messaggio)

        # 5: Codifica della stringa JSON in byte (UTF-8) e invio al server
        sock_service.sendall(messaggio.encode("UTF-8"))

        # 6: Registrazione del tempo di inizio subito dopo l'invio per misurare la latenza
        start_time_thread = time.time()

        # 7: Ricezione della risposta dal server (massimo 1024 byte)
        data = sock_service.recv(1024)

    # 8: Registrazione del tempo di fine e calcolo della durata della risposta per questo thread
    end_time_thread = time.time()
    print("Received: ", data.decode())
    print(f"{threading.current_thread().name} exec time = ", end_time_thread - start_time_thread)

# --- Punto di ingresso del programma ---
if __name__ == "__main__":
    start_time = time.time()  # Tempo di inizio totale del programma

    # 9: Creazione di una lista di oggetti Thread, ognuno puntato alla funzione genera_richieste
    threads = [
        threading.Thread(target=genera_richieste, args=(HOST, PORT))
        for _ in range(NUM_WORKERS)
    ]

    # 10: Avvio di tutti i thread creati (le richieste partono quasi simultaneamente)
    [thread.start() for thread in threads]

    # 11: Attesa della conclusione di tutti i thread prima di procedere oltre nel codice
    [thread.join() for thread in threads]

    end_time = time.time()  # Tempo di fine totale

    # Stampa il tempo complessivo impiegato per eseguire tutte le richieste
    print("Tempo totale impiegato = ", end_time - start_time)