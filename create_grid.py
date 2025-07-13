def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c

    return grid

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

# --- 함수 사용 예제 ---
# 2개의 완성된 줄이 있는 가상의 locked_pos 생성
locked_positions = {}
for j in range(10):
    locked_positions[(j, 19)] = (255, 0, 0)
    locked_positions[(j, 18)] = (255, 255, 0)
locked_positions[(5, 17)] = (0, 255, 0)

grid = create_grid(locked_positions)

print("줄을 지우기 전 locked_positions:", locked_positions)

rows_cleared = clear_rows(grid, locked_positions)
print(f"\n지워진 줄의 수: {rows_cleared}")
print("줄을 지운 후 locked_positions:", locked_positions)
