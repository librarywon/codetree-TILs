import sys
from collections import deque
import copy

input = sys.stdin.readline

# 방향 설정 (남, 서, 동, 북)
di = [1,0,0,-1]
dj = [0,-1,1,0]

R, C, K = map(int, input().split())

# 숲을 나타내는 격자
forest = [[0] * (C+2) for _ in range(R+2)]
for i in range(R+2):
    for j in range(C+2):
        if j==0 or j== C+1or i==R+1:
            forest[i][j] = 100


answer = 0
gol_cnt = 1


def print_forest(f):
    for i in f:
        print(i)
    print()

def clear_forest():
    global forest,gol_cnt
    gol_cnt = 1
    forest = [[0] * (C + 2) for _ in range(R + 2)]
    for i in range(R + 2):
        for j in range(C + 2):
            if j == 0 or j == C + 1 or i == R + 1:
                forest[i][j] = 100

def start_move(sj,sd):
    global gol_cnt
    si = -1
    sj = sj

    while True:
        # si, sj 기준 동서남북 좌표
        nsi, nsj = si -1, sj
        ssi, ssj = si +1, sj
        wsi, wsj = si, sj-1
        esi, esj = si, sj+1

        # -2이면 격자안에 하나밖에 검사 불가
        if si == -1:
            if forest[ssi+1][ssj] == 0:
                si = si +1
                continue
            # -2 인데 못내려가는 상황
            else:
                clear_forest()
                return False

        if si == R-1:
            break

        # 남 이동 검사 남 동 서 체크
        if not forest[ssi+1][ssj] and not forest[esi+1][esj] and not forest[wsi+1][wsj]:
                si +=1
                continue

        # 서 이동 검사 남 서 북 체크
        if not forest[ssi][ssj-1] and not forest[wsi][wsj-1]and not forest[nsi][nsj-1] :
            if not forest[ssi+1][ssj-1] and not forest[ssi][ssj-2]:
                si +=1
                sj -=1
                sd = (sd+3)%4
                continue

        # 동 이동 검사 남 동 북 체크
        if not forest[ssi][ssj + 1] and not forest[esi][esj + 1] and not forest[nsi][nsj + 1]:
            if not forest[ssi + 1][ssj + 1] and not forest[ssi][ssj + 2]:
                si += 1
                sj += 1
                sd = (sd+1)%4
                continue
        # 이제 이동 불가면 종료
        break

    # 모두 이동 했는데 여전히 밖이면?
    if si < 2:
        clear_forest()
        return False
    else:
        # 맵에 골램 위치 칠하기
        forest[si][sj] = gol_cnt
        for i in range(4):
            forest[si+di[i]][sj+dj[i]] = gol_cnt

        # 제대로 도착했다면 정령 내려서 좌표 반납
        if sd == 0:
            si = si-1
        elif sd == 1:
            sj = sj+1
        elif sd == 2:
            si = si+1
        elif sd == 3:
            sj = sj-1

        # 출구는 -
        forest[si][sj]= -forest[si][sj]

        return [si,sj]

def fairy_move(si,sj):
    global forest

    maxi = si
    visited = [[False]*(C+2) for _ in range(R+2)]
    Q = deque()
    Q.append([si,sj])
    visited[si][sj] = True

    while Q:
        ci, cj = Q.popleft()
        for k in range(4):
            ni = ci + di[k]
            nj = cj + dj[k]
            if ni <= 0 or ni >= R+1 or nj <= 0 or nj >= C+1:
                continue
            if forest[ni][nj]!=0 and not visited[ni][nj] and forest[ni][nj]!=100:
                if abs(forest[ni][nj]) == abs(forest[ci][cj]):
                    Q.append([ni,nj])
                    visited[ni][nj] = True
                    maxi = max(ni,maxi)
                elif abs(forest[ni][nj]) != abs(forest[ci][cj]) and forest[ci][cj] < 0 :
                    Q.append([ni, nj])
                    visited[ni][nj] = True
                    maxi = max(ni, maxi)
    return maxi

# 명령어 시작
for _ in range(K):
    fairyi, fairyd = map(int,input().split())

    fairy = start_move(fairyi,fairyd)

    # 숲에 못들어간 경우
    if not fairy:
        continue
    # 정령 이동
    fairyi, fairyj = fairy[0], fairy[1]

    answer += fairy_move(fairyi, fairyj)
    gol_cnt += 1

print(answer)