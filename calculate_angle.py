import numpy as np

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def calculate_distance(a, b):
    a = np.array(a)
    b = np.array(b)
    distance = np.linalg.norm(b - a)
    return distance

# --- 함수 사용 예제 ---
# 팔꿈치 각도 계산
shoulder = [10, 20, 0]
elbow = [15, 25, 0]
wrist = [20, 20, 0]
angle = calculate_angle(shoulder, elbow, wrist)
print(f"팔꿈치 각도: {angle:.2f}도")

# 두 점 사이의 거리 계산
nose = [10, 10, 0]
ankle = [10, 50, 0]
distance = calculate_distance(nose, ankle)
print(f"코와 발목 사이의 거리: {distance:.2f}")
