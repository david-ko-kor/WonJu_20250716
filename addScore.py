def add_score(rows):
    conversion = {
        0: 0,
        1: 40,
        2: 100,
        3: 300,
        4: 1200
    }
    return conversion.get(rows)

# --- 함수 사용 예제 ---
print(f"1줄 지웠을 때 점수: {add_score(1)}")
print(f"4줄 지웠을 때 점수: {add_score(4)}")
