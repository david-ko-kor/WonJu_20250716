# import cv2
# from PIL import ImageFont,ImageDraw,Image
# import numpy as np
# import os
# img=cv2.imread('nuddle.jpg',cv2.IMREAD_COLOR)
# height,width,color=img.shape
# print(width,height,color)
#
# new_width=400
# new_height=int(height*new_width/width)
# img_resized=cv2.resize(img,(new_width,new_height),interpolation=cv2.INTER_AREA)
# img_cartoon=cv2.stylization(img_resized,sigma_s=150,sigma_r=0.25)
# img_cartoon=cv2.ellipse(img_cartoon,(280,80),(100,60),0,0,360,(230,230,230),-1)
# print(img_cartoon)
# img_pillow=Image.fromarray(img_cartoon)
# print(type(img_pillow))
# font_paths = [
#     "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS 기본 한글 폰트
#     "/Library/Fonts/Arial Unicode MS.ttf",         # Arial Unicode (한글 지원)
#     "/System/Library/Fonts/Helvetica.ttc",        # Helvetica (영문 대체)
# ]
#
# font = None
# for font_path in font_paths:
#     try:
#         if os.path.exists(font_path):
#             font = ImageFont.truetype(font_path, 24)
#             print(f"폰트 로드 성공: {font_path}")
#             break
#     except Exception as e:
#         print(f"폰트 로드 실패 {font_path}: {e}")
#         continue
#
# if font is None:
#     print("기본 폰트를 사용합니다.")
#     font = ImageFont.load_default()
#
# b,g,r,a=0,0,0,255
# draw=ImageDraw.Draw(img_pillow,'RGBA')
# draw.text((200,70),"아니! 이맛은!!!!",font=font,fill=(b,g,r,a))
# img_numpy=np.array(img_pillow)
# print(type(img_numpy))
#
# cv2.imshow('test',img_cartoon)
# cv2.waitKey(0)
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import os

# 이미지 파일 존재 확인
if not os.path.exists('nuddle.jpg'):
    print("Error: nuddle.jpg 파일을 찾을 수 없습니다.")
    exit()

img = cv2.imread('nuddle.jpg', cv2.IMREAD_COLOR)
if img is None:
    print("Error: 이미지를 로드할 수 없습니다.")
    exit()

height, width, color = img.shape
print(f"이미지 크기: {width} x {height}, 채널: {color}")

new_width = 400
new_height = int(height * new_width / width)
img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
img_cartoon = cv2.stylization(img_resized, sigma_s=150, sigma_r=0.25)
img_cartoon = cv2.ellipse(img_cartoon, (280, 80), (100, 60), 0, 0, 360, (230, 230, 230), -1)

# BGR을 RGB로 변환 (OpenCV는 BGR, PIL은 RGB 사용)
img_cartoon_rgb = cv2.cvtColor(img_cartoon, cv2.COLOR_BGR2RGB)
img_pillow = Image.fromarray(img_cartoon_rgb)

# 맥용 한글 폰트 설정
font_paths = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS 기본 한글 폰트
    "/Library/Fonts/Arial Unicode MS.ttf",  # Arial Unicode (한글 지원)
    "/System/Library/Fonts/Helvetica.ttc",  # Helvetica (영문 대체)
]

font = None
for font_path in font_paths:
    try:
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 24)
            print(f"폰트 로드 성공: {font_path}")
            break
    except Exception as e:
        print(f"폰트 로드 실패 {font_path}: {e}")
        continue

if font is None:
    print("기본 폰트를 사용합니다.")
    font = ImageFont.load_default()

# 텍스트 추가
draw = ImageDraw.Draw(img_pillow)
draw.text((200, 70), "아니! 이맛은!!!!", font=font, fill=(0, 0, 0, 255))

# 결과 이미지 저장 (맥에서 cv2.imshow 문제 대신)
img_final = cv2.cvtColor(np.array(img_pillow), cv2.COLOR_RGB2BGR)
cv2.imwrite('newResult.jpg', img_final)
print("결과 이미지가 'result.jpg'로 저장되었습니다.")

# 맥에서 cv2.imshow 대신 matplotlib 사용 (선택사항)
# try:
#     import matplotlib.pyplot as plt
#
#     plt.figure(figsize=(10, 8))
#     plt.imshow(img_pillow)
#     plt.axis('off')
#     plt.title('Cartoon Effect with Text')
#     plt.show()
# except ImportError:
#     print("matplotlib이 설치되지 않았습니다. 이미지 파일을 확인하세요.")

# 또는 PIL로 직접 보기
# img_pillow.show()  # 기본 이미지 뷰어로 열림