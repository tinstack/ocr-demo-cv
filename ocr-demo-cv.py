import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont

# PaddleOCR 객체 생성
ocr = PaddleOCR(use_angle_cls=True, lang='korean')  # 한국어 인식

# 이미지 경로
image_path = './data/1.jpg'

# OCR 수행
result = ocr.ocr(image_path, cls=True)

# OpenCV로 이미지 로드 및 RGB 변환
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 이미지 크기 가져오기
img_height, img_width = image.shape[:2]

# 동적 폰트 크기 설정 (이미지 크기의 2%를 기본 폰트 크기로 설정)
base_font_size = max(int(img_height * 0.02), 12)  # 최소 12px 보장

# PIL Image 변환
image_pil = Image.fromarray(image)
draw = ImageDraw.Draw(image_pil)

# 한글 폰트 설정 (Windows 및 Mac/Linux 경로 다름)
font_path = "malgun.ttf"  # 윈도우: 'malgun.ttf', 맥: 'AppleGothic.ttf', 리눅스: '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font = ImageFont.truetype(font_path, base_font_size)  # 폰트 크기 설정

# Bounding Box 및 텍스트 표시
for line in result:
    for word_info in line:
        bbox = np.array(word_info[0], dtype=np.int32)
        text, score = word_info[1]

        # OpenCV로 Bounding Box 그리기
        draw.polygon([tuple(point) for point in bbox], outline="red", width=3)

        # PIL을 사용한 한글 텍스트 출력
        x, y = bbox[0]
        draw.text((x, y - 10), text, font=font, fill=(0, 255, 0))  # 초록색 텍스트

# 결과 이미지 출력
image_pil.show()

# 저장 (필요 시)
image_pil.save('output_with_korean_text.jpg')
