from deskew import determine_skew
from PIL import Image
import numpy as np
import os

# Đường dẫn tới folder chứa ảnh đầu vào và folder chứa ảnh đầu ra
input_folder = 'output_images_scan/'  # Đảm bảo thay thế bằng đường dẫn folder ảnh đầu vào
output_folder = 'output_images_deskew/'  # Đảm bảo thay thế bằng đường dẫn folder ảnh đầu ra

# Tạo folder đầu ra nếu chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Duyệt qua tất cả các file trong folder đầu vào
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    
    # Kiểm tra nếu là file ảnh
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        # Đọc ảnh gốc
        image = Image.open(input_path)
        image = image.convert('L')  # Chuyển ảnh sang ảnh xám

        # Tạo ảnh A3 với nền trắng (3508x4961 pixel tại 300 DPI)
        a3_width = 3508
        a3_height = 4961
        a3_image = Image.new('L', (a3_width, a3_height), color=255)  # Màu nền trắng

        # Đặt ảnh gốc vào giữa ảnh A3
        image_width, image_height = image.size
        left = (a3_width - image_width) // 2
        top = (a3_height - image_height) // 2
        a3_image.paste(image, (left, top))

        # Chuyển ảnh A3 thành mảng numpy
        a3_image_array = np.array(a3_image)

        # Xác định góc nghiêng của ảnh và xoay ảnh
        angle = determine_skew(a3_image_array)
        rotated_image = a3_image.rotate(angle, expand=True)

        # Sau khi xoay, tính toán crop từ trung tâm
        rotated_width, rotated_height = rotated_image.size
        crop_width = 2480  # A4 width at 300 DPI
        crop_height = 3508  # A4 height at 300 DPI

        # Tính toán tọa độ crop từ trung tâm
        left = (rotated_width - crop_width) // 2
        top = (rotated_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height

        # Crop ảnh từ trung tâm
        cropped_image = rotated_image.crop((left, top, right, bottom))

        # Lưu ảnh kết quả vào folder đầu ra
        output_path = os.path.join(output_folder, filename)
        cropped_image.save(output_path)

        # In ra kết quả
        print(f"Ảnh {filename} đã được làm thẳng với góc {angle} độ và đã crop từ trung tâm thành kích thước A4. Lưu tại: {output_path}")
