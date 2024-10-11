import sys
from collections import deque

input = sys.stdin.readline

# 우하좌상 이동 순서
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

n, m, h, k = map(int, input().split())
a = [[deque() for _ in range(n)] for _ in range(n)]
sx, sy, sd = n // 2, n // 2, 3  # 술래 처음 좌표와 이동 방향

# a에 도망자가 있는 위치에 이동방향을 값으로 저장
for _ in range(m):
    x, y, d = map(int, input().split())
    a[x-1][y-1].append(d-1)

# 나무가 있는 위치는 1로 tree에 저장
tree = [[0 for _ in range(n)] for _ in range(n)]
for _ in range(h):
    x, y = map(int, input().split())
    tree[x-1][y-1] = 1

# move: 술래가 이동한 거리
# rotate: 술래가 얼마만큼 이동했을때 회전하는지
# cnt: 몇 번 회전했는지
# forward: forward = 1 이면 가운데 좌표에서 [0, 0] 으로 이동. 0이면 반대로 이동
move, rotate, cnt, forward, ans = 0, 1, 0, 1, 0
for turn in range(k):
    # 현재 좌표에 도망자가 몇 명 있는지 len_a에 기록
    # 도망자는 동시에 이동하기 때문에, 중복 이동을 방지하기 위해 사용
    len_a = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            len_a[i][j] = len(a[i][j])

    # 도망자 이동
    for i in range(n):
        for j in range(n):
            if len_a != 0 and abs(sx - i) + abs(sy - j) <= 3:
                for _ in range(len_a[i][j]):
                    d = a[i][j].popleft()
                    nx = i + dx[d]
                    ny = j + dy[d]
                    # 범위를 벗어나면 방향을 반대로
                    if not 0 <= nx < n:
                        d = (d + 2) % 4
                        nx = i + dx[d]
                    if not 0 <= ny < n:
                        d = (d + 2) % 4
                        ny = j + dy[d]
                    # 다음 좌표에 술래가 있으면 이동하지 않는다
                    if nx == sx and ny == sy:
                        a[i][j].append(d)
                        continue
                    a[nx][ny].append(d)

    # 술래 이동
    sx += dx[sd]
    sy += dy[sd]
    move += 1
    # [n//2, n//2] -> [0, 0]
    if forward:
        if move == rotate:  # 회전해야하는 좌표에 도착
            move = 0
            sd = (sd + 1) % 4  # 시계방향 회전
            cnt += 1  # 회전한 횟수 증가
            if cnt == 2:  # 2번 회전하면 rotate를 증가하고 회전횟수 초기화
                cnt = 0
                rotate += 1
        if sx == 0 and sy == 0:  # forward 이동 도착지점
            sd = 1  # 아래방향으로 수정
            move, rotate, cnt, forward = 0, n-1, 0, 0
            # 역방향으로 이동할때만 처음에 n-1만큼 3번 이동해야 rotate를 바꿔야한다
            # back_first 변수를 따로 두어서 역방향 첫 회전때 회전한 횟수를 안늘리도록 함
            back_first = 1
    # [0, 0] -> [n//2, n//2]
    else:
        if move == rotate:
            move = 0
            sd = (sd + 3) % 4  # 반시계 방향 회전
            if not back_first:  # 처음 이동이 아니면 회전횟수 증가
                cnt += 1
            else:
                back_first = 0
            if cnt == 2: # 2번 회전하면 rotate를 감소하고 회전횟수 초기화
                cnt = 0
                rotate -= 1
        if sx == n // 2 and sy == n // 2:  # backward 이동 도착지점
            sd = 3  # 윗방향으로 수정
            move, rotate, cnt, forward = 0, 1, 0, 1

    # 술래 좌표포함 거리 3안에 있는 도망자 제거
    for i in range(3):
        nx = sx + i * dx[sd]
        ny = sy + i * dy[sd]
        if 0 <= nx < n and 0 <= ny < n:
            if tree[nx][ny] == 0:  # 나무가 없는 경우만 제거
                ans += (turn + 1) * len(a[nx][ny])
                a[nx][ny] = deque()
        else:
            break

print(ans)