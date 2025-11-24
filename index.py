import cv2
import easyocr
import numpy as np
from datetime import datetime

# Inisialisasi EasyOCR (hanya sekali)
print("Loading EasyOCR...")
reader = easyocr.Reader(['en'], gpu=True)  # Ubah gpu=True jika ada NVIDIA GPU

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Buat window yang bisa diresize
cv2.namedWindow('EasyOCR', cv2.WINDOW_NORMAL)
# Set ukuran default window (opsional)
cv2.resizeWindow('EasyOCR', 800, 600)

# Nama file output
output_file = "ocr_results.txt"

print("Tekan 'q' untuk keluar")
print("Tekan 's' untuk OCR")
print(f"Hasil OCR akan disimpan di: {output_file}")

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
        # Frame tetap resolusi asli (1280x720) meskipun window diresize
        results = reader.readtext(frame)
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simpan ke file .txt
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n=== OCR Result - {timestamp} ===\n")
            
            if results:
                for (bbox, text, prob) in results:
                    f.write(f"{text}\n")
                    print(f"{text}")
            else:
                f.write("Tidak ada teks terdeteksi\n")
                print("Tidak ada teks terdeteksi")
            
            f.write("=" * 50 + "\n")
        
        print(f"Hasil disimpan ke {output_file}\n")

cap.release()
cv2.destroyAllWindows()