import cv2
import numpy as np
import os

# Đường dẫn tới folder chứa ảnh đầu vào và folder chứa ảnh đầu ra
input_folder = 'input_images/'  # Đảm bảo thay thế bằng đường dẫn folder ảnh đầu vào
output_folder = 'output_images_scan/'  # Đảm bảo thay thế bằng đường dẫn folder ảnh đầu ra

# Tạo folder đầu ra nếu chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Duyệt qua tất cả các file trong folder đầu vào
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    
    # Kiểm tra nếu là file ảnh
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        # Đọc ảnh từ file
        image = cv2.imread(input_path)

        # Chuyển ảnh sang grayscale (ảnh xám)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Dùng Adaptive Threshold để phân tách nền và chữ tự nhiên hơn
        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, 
                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                               cv2.THRESH_BINARY, 
                                               31, 15)

        # Làm mịn nhẹ ảnh cho đẹp hơn
        final = cv2.medianBlur(adaptive_thresh, 3)

        # Lưu ảnh kết quả vào folder đầu ra
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, final)

        # In ra kết quả
        print(f"Ảnh đã được lưu tại: {output_path}")
