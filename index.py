import cv2
import easyocr
import numpy as np
from datetime import datetime

print("Loading EasyOCR...")
reader = easyocr.Reader(['en'], gpu=True)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow('EasyOCR - Monitor', cv2.WINDOW_NORMAL)
cv2.namedWindow('EasyOCR - Crop', cv2.WINDOW_NORMAL)
cv2.resizeWindow('EasyOCR - Monitor', 800, 600)
cv2.resizeWindow('EasyOCR - Crop', 640, 480)

output_file = "ocr_results.txt"

crop_x1, crop_y1 = 0, 0
crop_x2, crop_y2 = 1280, 720
is_selecting = False
temp_point = None
cropped_frame = None

def select_crop_area(event, x, y, flags, param):
    global crop_x1, crop_y1, crop_x2, crop_y2, is_selecting, temp_point
    
    height, width = param.shape[:2]
    
    if event == cv2.EVENT_LBUTTONDOWN:
        is_selecting = True
        crop_x1, crop_y1 = x, y
        temp_point = (x, y)
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_selecting:
            temp_point = (x, y)
    
    elif event == cv2.EVENT_LBUTTONUP:
        is_selecting = False
        crop_x2, crop_y2 = x, y
        crop_x1 = max(0, min(crop_x1, crop_x2))
        crop_x2 = min(width, max(crop_x1, crop_x2))
        crop_y1 = max(0, min(crop_y1, crop_y2))
        crop_y2 = min(height, max(crop_y1, crop_y2))

print("Tekan 'q' untuk keluar")
print("Tekan 's' untuk OCR")
print("Tekan 'c' untuk simpan crop area")
print("Tekan 'r' untuk reset crop ke full")
print("Drag mouse di window Crop untuk pilih area")
print(f"Hasil OCR akan disimpan di: {output_file}")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Gagal mengambil frame")
        break
    
    display_crop = frame.copy()
    
    cv2.rectangle(display_crop, (crop_x1, crop_y1), (crop_x2, crop_y2), (0, 255, 0), 2)
    
    if is_selecting and temp_point:
        cv2.rectangle(display_crop, (crop_x1, crop_y1), temp_point, (0, 255, 255), 2)
    
    if crop_x2 > crop_x1 and crop_y2 > crop_y1:
        cropped_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]
    else:
        cropped_frame = frame
    
    cv2.setMouseCallback('EasyOCR - Crop', select_crop_area, display_crop)
    
    cv2.imshow('EasyOCR - Monitor', frame)
    cv2.imshow('EasyOCR - Crop', display_crop)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        break
    elif key == ord('s'):
        print("\n[Processing OCR...]")
        
        results = reader.readtext(cropped_frame)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
    
    elif key == ord('c'):
        if cropped_frame is not None and cropped_frame.size > 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crop_{timestamp}.png"
            cv2.imwrite(filename, cropped_frame)
            print(f"Crop area disimpan: {filename}\n")
    
    elif key == ord('r'):
        crop_x1, crop_y1 = 0, 0
        crop_x2, crop_y2 = 1280, 720
        print("Crop area di-reset ke full\n")

cap.release()
cv2.destroyAllWindows()