import cv2
import pytesseract
import os

# Gunakan path instalasi Tesseract yang proper
# Jangan gunakan tesseract.exe di folder project
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cek apakah path valid
if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
    print("ERROR: Tesseract tidak ditemukan!")
    print("Install Tesseract dari: https://github.com/UB-Mannheim/tesseract/wiki")
    print("Pilih 'tesseract-ocr-w64-setup-5.3.3.20231005.exe' atau versi terbaru")
    exit(1)

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Atur resolusi kamera (opsional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Tekan 'q' untuk keluar")
print("Tekan 's' untuk OCR dan tampilkan teks")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Gagal mengambil frame dari kamera")
        break
    
    # Preprocessing untuk meningkatkan akurasi OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Tambahkan threshold untuk meningkatkan kontras
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # Tampilkan frame asli dan hasil preprocessing
    cv2.imshow('OCR Realtime - Original', frame)
    cv2.imshow('OCR Realtime - Processed', thresh)
    
    # Kontrol keyboard
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Trigger OCR saat tekan 's'
        print("\n[Processing OCR...]")
        try:
            text = pytesseract.image_to_string(thresh, lang='eng')
            print("=== HASIL OCR ===")
            if text.strip():
                print(text)
            else:
                print("Tidak ada teks terdeteksi")
            print("=================\n")
        except Exception as e:
            print(f"OCR Error: {e}\n")

# Cleanup
cap.release()
cv2.destroyAllWindows()