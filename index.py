import cv2
import easyocr
import numpy as np

# Inisialisasi EasyOCR (hanya sekali)
print("Loading EasyOCR...")
reader = easyocr.Reader(['en'], gpu=True)  # Ubah gpu=True jika ada NVIDIA GPU

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Tekan 'q' untuk keluar")
print("Tekan 's' untuk OCR")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Gagal mengambil frame")
        break
    
    cv2.imshow('EasyOCR', frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        break
    elif key == ord('s'):
        print("\n[Processing OCR...]")
        
        # OCR otomatis tanpa preprocessing
        results = reader.readtext(frame)
        
        print("=== HASIL OCR ===")
        if results:
            for (bbox, text, prob) in results:
                print(f"{text}")
        else:
            print("Tidak ada teks terdeteksi")
        print("=================\n")

cap.release()
cv2.destroyAllWindows()