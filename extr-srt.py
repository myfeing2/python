import os
import pytesseract
from PIL import Image

# 1. 配置路径
frame_dir = r"mp4/frames" 
output_file = "extracted_text.txt" 

# 2. 遍历所有帧图片
with open(output_file, "w", encoding="utf-8") as f:
    for img_name in os.listdir(frame_dir):
        if img_name.endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(frame_dir, img_name)
            img = Image.open(img_path)
            
            # 3. 裁剪目标区域
            cropped = img.crop((200, 300, 800, 500))  # left, top, right, bottom
            
            # 4. OCR识别
            text = pytesseract.image_to_string(cropped, lang="eng", config="--psm 6")
            # --psm 6: 强制按单行识别
            
            # 5.写入文件（一帧写入一行）
            cleaned_text = text.strip().replace("\n", " ")
            f.write(cleaned_text + "\n")

print(f"提取完成！结果保存在 {output_file}")
