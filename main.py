import cv2
import threading
import numpy as np
from datetime import datetime
import os
import platform
import time
import sys
import filtri

# Variabili globali per la visualizzazione su thread dedicato
imgf = None
lock = threading.Lock()
running = True

#visualizzazione dell'immagine in tempo reale  
def visualizza():
    global imgf, running
    while running:
        lock.acquire()
        if imgf is not None:
            cv2.imshow('img', imgf)
        lock.release()
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            running = False
            break

    cv2.destroyAllWindows()

#pulizia del terminale
def clear_screen():
    try:
        current_os = platform.system()
        if current_os == "Windows":
            os.system("cls")
        elif current_os in ("Linux", "Darwin"):  
            os.system("clear")
    except Exception as e:
        print(f"Errore durante la pulizia dello schermo: {e}")



if __name__ == "__main__":

    #data e ora dell'inizio delle modifiche, per log
    tempo = datetime.now()
    data_ora = tempo.strftime("%Y-%m-%d %H:%M:%S")

    #check degli argomenti passati da terminale
    if len(sys.argv) < 2:
        print("Uso improprio: python script.py <percorso_immagine>")
        exit()
    #inizializzazione dell'immagine
    image_path = sys.argv[1]
    img = cv2.imread(image_path)
    imgf = img.copy()
    img_history = [img.copy()]  # Per undo

    #inizializzazione log
    with open('Log.txt', 'a', encoding='utf-8') as file:
            file.write("\n" + f"{data_ora}\n")
            file.write("image: " + sys.argv[1] + "\n")

    # Avvio del thread per visualizzare l'immagine
    thread = threading.Thread(target=visualizza)
    thread.start()

    while running:
        clear_screen()
        print("\n--- MENU ---")
        print("1. Sharpening")
        print("2. Laplace")
        print("3. Mediano")
        print("4. Unsharp")
        print("5. Equalizzazione Istogramma")
        print("6. Bilaterale")
        print("u. Undo")
        print("e. Esci")
        scelta = input("Operazione scelta: ")

        lock.acquire()
 # 1. Sharpening
        if scelta == "1":
            n = int(input("Intensità (consigliato tra 4 e 9): ")) # input parametri

            imgf = filtri.sharpening(imgf,n) #chiamata funzione 
            
            img_history.append(imgf.copy()) # per undo

            # aggiornamento Log
            with open('Log.txt', 'a', encoding='utf-8') as file:
                file.write("sharpening intensità:" + str(n) + "\n")
# 2. LaPlace
        elif scelta == "2":
            n = int(input("dimensione kernel (dev'essere dispari): "))

            imgf = filtri.laplaciano(imgf,n)

            img_history.append(imgf.copy()) 

            with open('Log.txt', 'a', encoding='utf-8') as file:
                file.write("laplace kernel:" + str(n) + "\n")
# 3. Mediano
        elif scelta == "3":
             
            n = int(input("dimensione kernel (dev'essere dispari): "))

            imgf = filtri.mediano(imgf,n)

            img_history.append(imgf.copy())

            with open('Log.txt', 'a', encoding='utf-8') as file:
                file.write("mediano kernel:" + str(n) + "\n")
# 4. Unsharp Mask
        elif scelta == "4":

            dev = int(input("deviazione: "))            
            n = int(input("intensità: "))

            imgf = filtri.unsharp(imgf, dev, n)

            img_history.append(imgf.copy())

            with open('Log.txt', 'a', encoding='utf-8') as file:
                file.write("unsharp deviazione:" + str(dev) + "intensità:" + str(n) + "\n")

# 5. Equalizzazione dell'istogramma
        elif scelta == "5":
            
            imgf = filtri.histogram_equalization(imgf)

            img_history.append(imgf.copy())

            with open('Log.txt', 'a', encoding='utf-8') as file:
                file.write("equalizzazione istogramma" + "\n")
# 6. Bilaterale
        elif scelta == "6":
            d = int(input("diametro: "))
            devc = int(input("deviazione colore: "))            
            devs = int(input("deviazione spazio: "))

            imgf = filtri.bilaterale(imgf, d, devc, devs)

            img_history.append(imgf.copy())

            with open('Log.txt', 'a', encoding='utf-8') as file:
                file.write("bilaterale diametro:" + str(d) + "deviazione colore:" + str(devc) + "deviazione spazio:" + str(devs) + "\n")

# Undo
        elif scelta == "u" or scelta == "U":
            if len(img_history) > 1:
                img_history.pop()
                imgf = img_history[-1].copy()
                with open('Log.txt', 'a', encoding='utf-8') as file:
                    file.write("undo\n")
            else:
                print("Nessuna operazione da annullare.")
 # uscita           
        elif scelta == "e" or scelta == "E":
            print("Salvare?[y/n]")
            scelta1 = input()
            if scelta1 == "y":
                cv2.imwrite('output.png', imgf)
                with open('Log.txt', 'a', encoding='utf-8') as file:
                    file.write("saved" + "\n")
            clear_screen()
            running = False
        else:
            print("Operazione non valida.")
        lock.release()

    thread.join()