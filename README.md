# Progetto_Digital_Forensics
Progetto Digital Forensics - Raffaele Ernesto Cocomero

Tool interattivo per il miglioramento forense delle immagini:

permette di applicare e visualizzare in tempo reale filtri di miglioramento forense 
(Sharpening, Laplaciano, Mediano, Unsharp, Equalizzazione, Bilaterale) e l'annullamento
di eventuali modifiche attraverso la funzione Undo. <br> 
È composto da 2 file principali:
main.py: <br>
contiene menù e logica del tool


filtri.py: <br>
contiene le funzioni di applicazione del filtro attraverso la libreria OpenCV (cv2), separare
i filtri dalla logica del tool garantisce una maggiore modularità, permettendo in futuro una
facile gestione, modifica ed eventuale aggiunta di filtri.

Si tiene traccia delle operazioni applicate all'immagine nel file log.txt

## Prerequisiti
* Python 3.x
* OpenCV (`pip install opencv-python`)
* NumPy

## Uso
Per l'utilizzo del tool è necessario passare il percorso dell'immagine attraverso questa sintassi:

python main.py [percorso_immagine]

## Esempio di log

2025-11-05 22:15:08 <br> 
image: Lenna.png <br>
sharpening intensità:5 <br>
bilaterale diametro:9deviazione colore:75deviazione spazio:75 <br>
undo <br>
equalizzazione istogramma <br>
