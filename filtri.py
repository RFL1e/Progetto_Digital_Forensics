import cv2
import numpy as np

def sharpening(img,n):
    try: 
        # Definizione del kernel per il filtro convolutivo
        kernel = np.array([[0, -1, 0],
                           [-1, n, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(img, -1, kernel)
        return sharpened
    except ValueError:
        print("Input errato: inserire un numero intero.")
        time.sleep(3)
        return img


def laplaciano(img, kernel):
    try:
        kernel = int(max(3, kernel) // 2 * 2 + 1) # imposizione di kernel dispari

        # conversione in scala di grigi
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        
        # applicazione del filtro laplaciano
        laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=kernel)
        
        # Conversione in formato visualizzabile (uint8)
        laplacian = cv2.convertScaleAbs(laplacian)
        
        return laplacian
    except Exception as e:
        print(f"Errore: {e}")
        return img

def mediano(img, kernel):
    try:
        kernel = int(max(3, kernel) // 2 * 2 + 1) # imposizione di kernel dispari
        if img.ndim == 2:
            return cv2.medianBlur(img, kernel)
        
        # Per immagini a colori: applicazione del filtro separatamente su ogni canale
        channels = cv2.split(img)
        den = [cv2.medianBlur(c, kernel) for c in channels]
        return cv2.merge(den)
    except Exception as e:
        print(f"Errore: {e}")
        return img

def unsharp(img, dev, n):
    try:
        blurred = cv2.GaussianBlur(img, (0, 0), dev)
        return cv2.addWeighted(img, 1 + n, blurred, -n, 0)
    except Exception as e:
        print(f"Errore Unsharp Masking: {e}")
        return img

def histogram_equalization(img):
    try:
        if len(img.shape) == 2:
            return cv2.equalizeHist(img)

        # Per immagini a colori: conversione da RGB a YUV
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        #Applicazione dell'equalizzazione sul canale Y (luminanza)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    except Exception as e:
        print(f"Errore Equalizzazione: {e}")
        return img

def bilaterale(img, d, devc, devs):
    try:
        return cv2.bilateralFilter(img, d, devc, devs)
    except Exception as e:
        print(f"Errore Filtro Bilaterale: {e}")
        return img
